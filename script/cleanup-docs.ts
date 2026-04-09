// scripts/cleanup-docs.ts
// 清理脚本：检查并删除在 docs.json 中未被引用的 .mdx 文件

import * as fs from 'fs/promises';
import * as path from 'path';
import * as readline from 'readline';

const ROOT_DIR = path.resolve(__dirname, '..');

// 需要扫描的目录
const SCAN_DIRS = ['en', 'cn', 'jp', 'ko', 'zh-Hant'];

// 需要排除的目录（这些目录下的文件不会被检查）
const EXCLUDED_DIRS = [
  'node_modules',
  '.git',
  'script',
  'images',
  'logo',
  'snippets',
];

// 需要排除的文件（这些文件即使未被引用也不会被删除）
const EXCLUDED_FILES = [
  'i18n.key.md',
];

/**
 * 递归提取 docs.json 中所有被引用的页面路径
 */
function extractReferencedPages(obj: any, pages: Set<string>): void {
  if (Array.isArray(obj)) {
    for (const item of obj) {
      extractReferencedPages(item, pages);
    }
  } else if (typeof obj === 'object' && obj !== null) {
    // 如果有 pages 属性，递归处理
    if (obj.pages) {
      extractReferencedPages(obj.pages, pages);
    }
    // 如果有 groups 属性，递归处理
    if (obj.groups) {
      extractReferencedPages(obj.groups, pages);
    }
    // 如果有 tabs 属性，递归处理
    if (obj.tabs) {
      extractReferencedPages(obj.tabs, pages);
    }
    // 如果有 languages 属性，递归处理
    if (obj.languages) {
      extractReferencedPages(obj.languages, pages);
    }
    // 如果有 navigation 属性，递归处理
    if (obj.navigation) {
      extractReferencedPages(obj.navigation, pages);
    }
  } else if (typeof obj === 'string') {
    // 这是一个页面路径
    pages.add(obj);
  }
}

/**
 * 递归扫描目录，获取所有 .mdx 文件
 */
async function scanDirectory(dir: string, files: string[]): Promise<void> {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    const relativePath = path.relative(ROOT_DIR, fullPath);
    
    // 跳过排除的目录
    if (entry.isDirectory()) {
      if (EXCLUDED_DIRS.includes(entry.name)) {
        continue;
      }
      await scanDirectory(fullPath, files);
    } else if (entry.isFile()) {
      // 跳过排除的文件
      if (EXCLUDED_FILES.includes(entry.name)) {
        continue;
      }
      // 只处理 .mdx 文件
      if (entry.name.endsWith('.mdx')) {
        files.push(relativePath);
      }
    }
  }
}

/**
 * 询问用户确认
 */
async function askConfirmation(question: string): Promise<boolean> {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes');
    });
  });
}

async function main() {
  console.log('🔍 开始扫描未被引用的文件...\n');
  
  try {
    // 1. 读取 docs.json
    const docsContent = await fs.readFile(path.join(ROOT_DIR, 'docs.json'), 'utf-8');
    const docsJson = JSON.parse(docsContent);
    
    // 2. 提取所有被引用的页面
    const referencedPages = new Set<string>();
    extractReferencedPages(docsJson, referencedPages);
    
    // 转换为带 .mdx 后缀的路径集合
    const referencedFiles = new Set<string>();
    for (const page of referencedPages) {
      referencedFiles.add(`${page}.mdx`);
    }
    
    console.log(`📄 docs.json 中引用了 ${referencedFiles.size} 个页面\n`);
    
    // 3. 扫描目录获取所有 .mdx 文件
    const allFiles: string[] = [];
    for (const dir of SCAN_DIRS) {
      const scanPath = path.join(ROOT_DIR, dir);
      try {
        await fs.access(scanPath);
        await scanDirectory(scanPath, allFiles);
      } catch {
        console.log(`⚠️  目录 ${dir} 不存在，跳过`);
      }
    }
    
    console.log(`📁 扫描到 ${allFiles.length} 个 .mdx 文件\n`);
    
    // 4. 找出未被引用的文件
    const unreferencedFiles: string[] = [];
    for (const file of allFiles) {
      if (!referencedFiles.has(file)) {
        unreferencedFiles.push(file);
      }
    }
    
    if (unreferencedFiles.length === 0) {
      console.log('✅ 没有发现未被引用的文件，一切正常！');
      return;
    }
    
    // 5. 显示未被引用的文件列表
    console.log(`⚠️  发现 ${unreferencedFiles.length} 个未被引用的文件：\n`);
    for (const file of unreferencedFiles) {
      console.log(`   - ${file}`);
    }
    console.log('');
    
    // 6. 检查是否有 --dry-run 或 --force 参数
    const args = process.argv.slice(2);
    const isDryRun = args.includes('--dry-run');
    const isForce = args.includes('--force');
    
    if (isDryRun) {
      console.log('📝 这是 dry-run 模式，不会实际删除文件');
      return;
    }
    
    // 7. 询问用户是否删除
    let shouldDelete = isForce;
    if (!isForce) {
      shouldDelete = await askConfirmation('是否删除这些文件？(y/N): ');
    }
    
    if (!shouldDelete) {
      console.log('❌ 已取消删除操作');
      return;
    }
    
    // 8. 删除文件
    console.log('\n🗑️  正在删除文件...\n');
    let deletedCount = 0;
    let errorCount = 0;
    
    for (const file of unreferencedFiles) {
      const fullPath = path.join(ROOT_DIR, file);
      try {
        await fs.unlink(fullPath);
        console.log(`   ✓ 已删除: ${file}`);
        deletedCount++;
      } catch (error) {
        console.log(`   ✗ 删除失败: ${file} - ${error}`);
        errorCount++;
      }
    }
    
    // 9. 清理空目录
    console.log('\n🧹 正在清理空目录...\n');
    await cleanEmptyDirs(ROOT_DIR);
    
    console.log(`\n✅ 完成！删除了 ${deletedCount} 个文件，${errorCount} 个文件删除失败`);
    
  } catch (error) {
    console.error('❌ 发生错误:', error);
    process.exit(1);
  }
}

/**
 * 递归清理空目录
 */
async function cleanEmptyDirs(dir: string): Promise<boolean> {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  
  // 跳过排除的目录
  const dirName = path.basename(dir);
  if (EXCLUDED_DIRS.includes(dirName)) {
    return false;
  }
  
  let isEmpty = true;
  
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    
    if (entry.isDirectory()) {
      const subDirEmpty = await cleanEmptyDirs(fullPath);
      if (!subDirEmpty) {
        isEmpty = false;
      }
    } else {
      isEmpty = false;
    }
  }
  
  // 如果目录为空且不是根目录，删除它
  if (isEmpty && dir !== ROOT_DIR) {
    try {
      await fs.rmdir(dir);
      const relativePath = path.relative(ROOT_DIR, dir);
      console.log(`   ✓ 已删除空目录: ${relativePath}`);
      return true;
    } catch {
      return false;
    }
  }
  
  return isEmpty;
}

// 显示帮助信息
if (process.argv.includes('--help') || process.argv.includes('-h')) {
  console.log(`
清理脚本 - 删除 docs.json 中未被引用的 .mdx 文件

用法:
  npx ts-node script/cleanup-docs.ts [选项]

选项:
  --dry-run    只显示未被引用的文件，不实际删除
  --force      不询问确认，直接删除
  --help, -h   显示帮助信息

示例:
  npx ts-node script/cleanup-docs.ts --dry-run   # 查看哪些文件会被删除
  npx ts-node script/cleanup-docs.ts             # 交互式删除
  npx ts-node script/cleanup-docs.ts --force     # 强制删除
`);
  process.exit(0);
}

main();
