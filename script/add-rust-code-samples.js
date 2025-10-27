const fs = require('fs');
const path = require('path');

// Rust代码示例模板
const rustTemplates = {
  // GET请求模板
  get: (endpoint, params = []) => {
    const queryParams = params.filter(p => p.in === 'query').map(p => `${p.name}={${p.name}}`).join('&');
    const queryString = queryParams ? `?${queryParams}` : '';
    
    return `use reqwest::Client;
use serde_json::Value;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::new();
    
    let response = client
        .get("https://api.chainstream.io${endpoint}${queryString}")
        .header("Authorization", "Bearer YOUR_ACCESS_TOKEN")
        .send()
        .await?;
    
    let data: Value = response.json().await?;
    println!("{:?}", data);
    
    Ok(())
}`;
  },

  // POST请求模板
  post: (endpoint, bodySchema = null) => {
    let bodyCode = '';
    if (bodySchema) {
      bodyCode = `
    let body = serde_json::json!({
        // Add your request body here based on the schema
    });`;
    }

    return `use reqwest::Client;
use serde_json::Value;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::new();${bodyCode}
    
    let response = client
        .post("https://api.chainstream.io${endpoint}")
        .header("Authorization", "Bearer YOUR_ACCESS_TOKEN")
        .header("Content-Type", "application/json")${bodySchema ? '\n        .json(&body)' : ''}
        .send()
        .await?;
    
    let data: Value = response.json().await?;
    println!("{:?}", data);
    
    Ok(())
}`;
  }
};

// 生成Rust代码示例
function generateRustCodeSample(operation, path, parameters = [], requestBody = null) {
  const method = operation.toLowerCase();
  
  if (method === 'get') {
    return rustTemplates.get(path, parameters);
  } else if (method === 'post') {
    return rustTemplates.post(path, requestBody);
  } else if (method === 'put') {
    return rustTemplates.post(path, requestBody); // 使用POST模板
  } else if (method === 'delete') {
    return rustTemplates.get(path, parameters); // 使用GET模板
  }
  
  return rustTemplates.get(path, parameters);
}

// 处理OpenAPI文件
function addRustCodeSamples(filePath) {
  console.log(`Processing ${filePath}...`);
  
  const content = fs.readFileSync(filePath, 'utf8');
  const openapi = JSON.parse(content);
  
  let modified = false;
  
  // 遍历所有路径
  for (const [path, pathItem] of Object.entries(openapi.paths)) {
    // 遍历所有HTTP方法
    for (const [method, operation] of Object.entries(pathItem)) {
      if (typeof operation === 'object' && operation.operationId) {
        // 检查是否已经有x-codeSamples
        if (!operation['x-codeSamples']) {
          operation['x-codeSamples'] = [];
        }
        
        // 检查是否已经有Rust示例
        const hasRust = operation['x-codeSamples'].some(sample => sample.lang === 'Rust');
        
        if (!hasRust) {
          const rustCode = generateRustCodeSample(
            method, 
            path, 
            operation.parameters || [],
            operation.requestBody
          );
          
          operation['x-codeSamples'].push({
            lang: 'Rust',
            source: rustCode
          });
          
          modified = true;
          console.log(`Added Rust code sample for ${method.toUpperCase()} ${path}`);
        }
      }
    }
  }
  
  if (modified) {
    // 写入文件
    fs.writeFileSync(filePath, JSON.stringify(openapi, null, 2));
    console.log(`✅ Updated ${filePath} with Rust code samples`);
  } else {
    console.log(`ℹ️  No changes needed for ${filePath}`);
  }
}

// 主函数
function main() {
  const openapiFiles = [
    'en/api-reference/openapi-en.json',
    'cn/api-reference/openapi-cn.json'
  ];
  
  for (const file of openapiFiles) {
    if (fs.existsSync(file)) {
      addRustCodeSamples(file);
    } else {
      console.log(`⚠️  File not found: ${file}`);
    }
  }
}

// 运行脚本
if (require.main === module) {
  main();
}

module.exports = { addRustCodeSamples, generateRustCodeSample }; 