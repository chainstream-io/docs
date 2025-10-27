import * as fs from 'fs/promises';
import * as path from 'path';

interface I18nKeys {
  [key: string]: string;
}

interface Language {
  code: string;
  baseDir: string;
}

const SUPPORTED_LANGUAGES: Language[] = [
  { code: 'en', baseDir: 'en' },
  { code: 'cn', baseDir: 'cn' }
];

const ROOT_DIR = path.resolve(__dirname, '..');

async function parseI18nKeyFile(filePath: string): Promise<I18nKeys> {
  try {
    const content = await fs.readFile(filePath, 'utf-8');
    const keys: I18nKeys = {};
    
    const lines = content.split('\n');
    for (const line of lines) {
      if (!line.trim() || line.startsWith('//')) continue; // 跳过空行和注释
      
      // 修改正则表达式以匹配 KEY='value' 或 KEY="value" 格式
      const singleQuoteMatch = line.match(/^([^=]+)='([^']+)'$/);
      const doubleQuoteMatch = line.match(/^([^=]+)="([^"]+)"$/);
      
      if (singleQuoteMatch) {
        const [, key, value] = singleQuoteMatch;
        keys[key.trim()] = value.trim();
      } else if (doubleQuoteMatch) {
        const [, key, value] = doubleQuoteMatch;
        keys[key.trim()] = value.trim();
      } else {
        console.log(`No match for line: "${line}"`);
      }
    }
    return keys;
  } catch (error) {
    console.error(`Error parsing i18n key file: ${filePath}`, error);
    return {};
  }
}

async function processDescription(obj: any, i18nKeys: I18nKeys): Promise<void> {
  if (obj && typeof obj === 'object') {
    for (const key in obj) {
      if (typeof obj[key] === 'object') {
        await processDescription(obj[key], i18nKeys);
      } else if ((key === 'description' || key === 'summary') && typeof obj[key] === 'string') {
        const translationKey = obj[key];
        
        // 检查键值是否只包含大写字母、点号、下划线和数字
        const isValidKey = /^[A-Z0-9._]+$/.test(translationKey);
        
        if (isValidKey && i18nKeys[translationKey]) {
          obj[key] = i18nKeys[translationKey];
        } else if (isValidKey) {
          console.log(`No translation found for key: "${translationKey}"`);
        }
      }
    }
  }
}

async function processLanguage(language: Language) {
  try {
    // 读取 i18n key 文件
    const i18nKeyPath = path.join(ROOT_DIR, language.baseDir, 'api-reference', 'i18n.key.md');
    const i18nKeys = await parseI18nKeyFile(i18nKeyPath);

    // 读取 OpenAPI 文件
    const openapiPath = path.join(ROOT_DIR, language.baseDir, 'api-reference', `openapi-${language.code}.json`);
    const openapiContent = await fs.readFile(openapiPath, 'utf-8');
    const openapi = JSON.parse(openapiContent);

    // 处理所有 description 字段
    await processDescription(openapi, i18nKeys);

    // 写回处理后的 OpenAPI 文件
    await fs.writeFile(
      openapiPath,
      JSON.stringify(openapi, null, 2)
    );

    console.log(`Successfully processed ${language.code} translations`);
  } catch (error) {
    console.error(`Error processing ${language.code}:`, error);
  }
}

async function main() {
  try {
    for (const language of SUPPORTED_LANGUAGES) {
      await processLanguage(language);
    }
    console.log('All languages processed successfully');
  } catch (error) {
    console.error('Error in main process:', error);
  }
}

main().catch(console.error); 