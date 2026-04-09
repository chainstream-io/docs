import * as path from 'path';

export interface ServiceConfig {
  name: string;
  groupName: string;
  openapiFilePrefix: string;
  i18nFile: string;
  endpointSubDir: string;
}

export interface Language {
  code: string;
  baseDir: string;
}

export const SUPPORTED_LANGUAGES: Language[] = [
  { code: 'en', baseDir: 'en' },
  { code: 'cn', baseDir: 'cn' },
  { code: 'jp', baseDir: 'jp' },
  { code: 'ko', baseDir: 'ko' },
  { code: 'zh-Hant', baseDir: 'zh-Hant' },
];

export const SERVICES: ServiceConfig[] = [
  {
    name: 'data',
    groupName: 'DATA API',
    openapiFilePrefix: 'openapi-data',
    i18nFile: 'i18n-data.key.md',
    endpointSubDir: 'data',
  },
  {
    name: 'defi',
    groupName: 'DEFI API',
    openapiFilePrefix: 'openapi-defi',
    i18nFile: 'i18n-defi.key.md',
    endpointSubDir: 'defi',
  },
];

export const EXCLUDED_TAGS: string[] = ['Job'];

export const ROOT_DIR = path.resolve(__dirname, '..');

export function getOpenapiFileName(service: ServiceConfig, langCode: string): string {
  return `${service.openapiFilePrefix}-${langCode}.json`;
}

export function getOpenapiPath(service: ServiceConfig, lang: Language): string {
  return path.join(ROOT_DIR, lang.baseDir, 'api-reference', getOpenapiFileName(service, lang.code));
}

export function getI18nPath(service: ServiceConfig, lang: Language): string {
  return path.join(ROOT_DIR, lang.baseDir, 'api-reference', service.i18nFile);
}

/**
 * Parse --service flag from process.argv.
 * Returns filtered SERVICES array. If no --service flag, returns all services.
 */
export function getSelectedServices(): ServiceConfig[] {
  const args = process.argv.slice(2);
  const serviceIdx = args.indexOf('--service');
  if (serviceIdx === -1 || serviceIdx + 1 >= args.length) {
    return SERVICES;
  }
  const serviceName = args[serviceIdx + 1].toLowerCase();
  const matched = SERVICES.filter(s => s.name === serviceName);
  if (matched.length === 0) {
    const valid = SERVICES.map(s => s.name).join(', ');
    console.error(`Unknown service "${serviceName}". Valid services: ${valid}`);
    process.exit(1);
  }
  return matched;
}
