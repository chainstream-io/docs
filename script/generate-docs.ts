// scripts/generate-docs.ts
import * as fs from 'fs/promises';
import * as path from 'path';

interface OpenAPIObject {
  paths: {
    [path: string]: PathItemObject;
  };
}

interface PathItemObject {
  [method: string]: OperationObject | any;
}

interface OperationObject {
  tags?: string[];
  summary?: string;
  description?: string;
  operationId?: string;
}

interface PathInfo {
  path: string;
  method: string;
  operation: OperationObject;
}

interface Language {
  code: string;
  baseDir: string;
}

const SUPPORTED_LANGUAGES: Language[] = [
  { code: 'en', baseDir: 'en' },
  { code: 'cn', baseDir: 'cn' }
];

// 需要排除的 Controller（tag），这些 Controller 的接口不会生成文档
const EXCLUDED_TAGS: string[] = [
  // 'ExampleController',  // 示例：添加需要排除的 Controller 名称
  'Jobs',
];

// 添加根目录路径常量
const ROOT_DIR = path.resolve(__dirname, '..');

async function processDescription(obj: any, language: string): Promise<void> {
  if (obj && typeof obj === 'object') {
    for (const key in obj) {
      if (typeof obj[key] === 'object') {
        await processDescription(obj[key], language);
      } else if (key === 'description' && typeof obj[key] === 'string') {
        const descriptions = obj[key].split(';');
        for (const desc of descriptions) {
          const trimmedDesc = desc.trim();
          if (trimmedDesc.startsWith(`${language}:`)) {
            obj[key] = trimmedDesc.substring(language.length + 1).trim();
            break;
          }
        }
      }
    }
  }
}

async function updateOpenAPIDescriptions() {
  for (const language of SUPPORTED_LANGUAGES) {
    const openapiPath = path.join(ROOT_DIR, language.baseDir, 'api-reference', 'openapi.json');
    
    try {
      // 读取 openapi.json
      const openapiContent = await fs.readFile(openapiPath, 'utf-8');
      const openapi = JSON.parse(openapiContent);

      // 处理所有 description 字段
      await processDescription(openapi, language.code);

      // 写回文件
      await fs.writeFile(
        openapiPath,
        JSON.stringify(openapi, null, 2)
      );
      console.log(`Updated descriptions in ${language.code}/api-reference/openapi.json`);
    } catch (error) {
      console.error(`Error processing ${language.code} openapi.json:`, error);
    }
  }
}

async function generateDocs() {
  try {
    // 1. 读取现有的 docs.json
    const docsContent = await fs.readFile(path.join(ROOT_DIR, 'docs.json'), 'utf-8');
    const docsJson = JSON.parse(docsContent);

    // 2. 为每种语言生成文档
    for (const language of SUPPORTED_LANGUAGES) {
      // 读取对应语言的 openapi.json
      let openapi: OpenAPIObject;
      try {
        const openapiContent = await fs.readFile(
          path.join(ROOT_DIR, language.baseDir, 'api-reference', `openapi-${language.code}.json`), 
          'utf-8'
        );
        openapi = JSON.parse(openapiContent);
      } catch (error) {
        console.error(`无法找到 ${language.code} 的 openapi.json 文件`);
        console.error('期望路径:', path.join(ROOT_DIR, language.baseDir, 'api-reference', 'openapi.json'));
        continue; // 跳过这个语言，继续处理其他语言
      }

      // 3. 解析所有路径，按 tag 分组
      const pathsByTag = new Map<string, PathInfo[]>();

      for (const [path, pathItem] of Object.entries(openapi.paths)) {
        for (const [method, operation] of Object.entries(pathItem)) {
          if (method === 'parameters') continue;
          
          const op = operation as OperationObject;
          if (!op.tags?.length) continue;
          
          const tag = op.tags[0];
          if (!pathsByTag.has(tag)) {
            pathsByTag.set(tag, []);
          }
          pathsByTag.get(tag)?.push({ path, method, operation: op });
        }
      }

      // 4. 生成 MDX 文件
      for (const [tag, operations] of pathsByTag) {
        // 检查是否在排除列表中
        if (EXCLUDED_TAGS.includes(tag)) {
          console.log(`Skipped tag: ${tag} (in EXCLUDED_TAGS)`);
          continue;
        }
        
        const tagDir = path.join(ROOT_DIR, language.baseDir, 'api-reference', 'endpoint', tag.toLowerCase());
        await fs.mkdir(tagDir, { recursive: true });

        for (const { path: apiPath, method, operation } of operations) {
          const fileName = generateFileName(apiPath, method);
          const mdxContent = generateMDXContent(apiPath, method, operation, language.code);
          
          // 检查是否有版本号，如果有则创建版本文件夹
          const version = getVersionFromPath(apiPath);
          let filePath;
          
          if (version) {
            const versionDir = path.join(tagDir, `v${version}`);
            await fs.mkdir(versionDir, { recursive: true });
            filePath = path.join(versionDir, `${fileName}.mdx`);
          } else {
            filePath = path.join(tagDir, `${fileName}.mdx`);
          }
          
          // 检查文件是否已存在，如果存在则跳过
          try {
            await fs.access(filePath);
            console.log(`Skipped ${language.code}: ${filePath} (already exists)`);
            continue;
          } catch {
            // 文件不存在，继续生成
          }
          
          await fs.writeFile(filePath, mdxContent);
          console.log(`Generated ${language.code}: ${filePath}`);
        }
      }

      // 5. 更新 docs.json 中的 API Reference
      const apiReferenceTab = docsJson.navigation.tabs.find((tab: any) => tab.tab === "API Reference");
      if (apiReferenceTab && apiReferenceTab.languages) {
        const langConfig = apiReferenceTab.languages.find((l: any) => l.language === language.code);
        if (langConfig) {
          const dexApiGroup = langConfig.groups.find((group: any) => 
            group.group === 'REST API'
          );

          if (dexApiGroup) {
            // 更新每个标签的页面
            for (const [tag, operations] of pathsByTag) {
              // 跳过排除列表中的 tag
              if (EXCLUDED_TAGS.includes(tag)) {
                continue;
              }
              
              const pages = operations.map(op => {
                const fileName = generateFileName(op.path, op.method);
                const version = getVersionFromPath(op.path);
                
                if (version) {
                  return `${language.code}/api-reference/endpoint/${tag.toLowerCase()}/v${version}/${fileName}`;
                } else {
                  return `${language.code}/api-reference/endpoint/${tag.toLowerCase()}/${fileName}`;
                }
              });
              
              // 检查 tag 是否包含多级目录（使用 / 分隔）
              if (tag.includes('/')) {
                // 多级 tag，使用嵌套结构
                const tagParts = tag.split('/');
                findOrCreateNestedGroup(dexApiGroup.pages, tagParts, pages);
              } else {
                // 单级 tag，使用原有逻辑
                const tagGroup = {
                  group: tag,
                  pages: pages
                };
                
                // 查找或创建标签组
                const existingGroupIndex = dexApiGroup.pages.findIndex((page: any) => 
                  page.group === tag
                );
                
                if (existingGroupIndex >= 0) {
                  dexApiGroup.pages[existingGroupIndex] = tagGroup;
                } else {
                  dexApiGroup.pages.push(tagGroup);
                }
              }
            }
          }
        }
      }
    }

    // 6. 写回 docs.json
    await fs.writeFile(
      path.join(ROOT_DIR, 'docs.json'),
      JSON.stringify(docsJson, null, 2)
    );
    console.log('Updated: docs.json');

    // 在完成文档生成后，处理 description 字段
    // await updateOpenAPIDescriptions();

  } catch (error) {
    console.error('Error generating docs:', error);
  }
}

function generateFileName(path: string, method: string): string {
  const baseName = path
    .replace(/^\//, '')
    .replace(/^v\d+\//, '') // 移除版本号前缀
    .replace(/\//g, '-')
    .replace(/[{}]/g, '')
    .toLowerCase();
  
  // 根据HTTP方法添加后缀，避免不同方法生成相同文件名
  const methodSuffix = method.toLowerCase();
  return `${baseName}-${methodSuffix}`;
}

function getVersionFromPath(path: string): string | null {
  const match = path.match(/^\/?v(\d+)\//);
  return match ? match[1] : null;
}

function generateMDXContent(path: string, method: string, operation: OperationObject, language: string): string {
  const openapiPath = `/${language}/api-reference/openapi-${language}.json`;
  return `---
title: '${operation.summary || path}'
openapi: '${openapiPath} ${method.toUpperCase()} ${path}'
---`;
}

/**
 * 在嵌套结构中查找或创建多级 group
 * 例如：tag = "Defi/sol/Moonshot" 会创建：
 * { group: "Defi", pages: [{ group: "sol", pages: [{ group: "Moonshot", pages: [...] }] }] }
 */
function findOrCreateNestedGroup(pages: any[], tagParts: string[], leafPages: string[]): void {
  if (tagParts.length === 0) return;
  
  const currentPart = tagParts[0];
  const remainingParts = tagParts.slice(1);
  
  // 查找当前层级的 group
  let existingGroup = pages.find((page: any) => page.group === currentPart);
  
  if (!existingGroup) {
    // 创建新的 group
    existingGroup = {
      group: currentPart,
      pages: []
    };
    pages.push(existingGroup);
  }
  
  if (remainingParts.length === 0) {
    // 这是最后一层，设置页面
    existingGroup.pages = leafPages;
  } else {
    // 还有更多层级，递归处理
    // 确保 pages 是数组（可能之前是字符串数组的页面列表）
    if (!Array.isArray(existingGroup.pages) || 
        (existingGroup.pages.length > 0 && typeof existingGroup.pages[0] === 'string')) {
      existingGroup.pages = [];
    }
    findOrCreateNestedGroup(existingGroup.pages, remainingParts, leafPages);
  }
}

generateDocs().catch(console.error);