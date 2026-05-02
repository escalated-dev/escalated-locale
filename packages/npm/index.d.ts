export type LocaleTree = Record<string, unknown>;

export declare function getLocaleData(locale?: string): LocaleTree;
export declare function t(
  key: string,
  locale?: string,
  params?: Record<string, string | number | boolean>
): string;
