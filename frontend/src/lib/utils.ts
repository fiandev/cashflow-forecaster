import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { marked } from "marked";
import DOMPurify from "dompurify";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(amount: number, currency: string = 'USD'): string {
  // Define currency symbol mapping
  const currencySymbols: Record<string, string> = {
    'USD': '$',    // US Dollar
    'EUR': '€',    // Euro
    'GBP': '£',    // British Pound
    'JPY': '¥',    // Japanese Yen
    'CAD': 'C$',   // Canadian Dollar
    'AUD': 'A$',   // Australian Dollar
    'CHF': 'Fr',   // Swiss Franc
    'CNY': '¥',    // Chinese Yuan
    'INR': '₹',    // Indian Rupee
    'KRW': '₩',    // South Korean Won
    'RUB': '₽',    // Russian Ruble
    'BRL': 'R$',   // Brazilian Real
    'MXN': 'Mex$', // Mexican Peso
    'SGD': 'S$',   // Singapore Dollar
    'NZD': 'NZ$',  // New Zealand Dollar
    'HKD': 'HK$',  // Hong Kong Dollar
    'NOK': 'kr',   // Norwegian Krone
    'SEK': 'kr',   // Swedish Krona
    'DKK': 'kr',   // Danish Krone
    'PLN': 'zł',   // Polish Zloty
    'CZK': 'Kč',   // Czech Koruna
    'HUF': 'Ft',   // Hungarian Forint
    'ILS': '₪',    // Israeli Shekel
    'TRY': '₺',    // Turkish Lira
    'ZAR': 'R',    // South African Rand
    'CLP': 'CLP$', // Chilean Peso
    'COP': 'COL$', // Colombian Peso
    'ARS': 'AR$',  // Argentine Peso
    'EGP': 'E£',   // Egyptian Pound
    'MYR': 'RM',   // Malaysian Ringgit
    'THB': '฿',    // Thai Baht
    'PHP': '₱',    // Philippine Peso
    'IDR': 'Rp',   // Indonesian Rupiah
    'VND': '₫',    // Vietnamese Dong
    'UAH': '₴',    // Ukrainian Hryvnia
    'AED': 'د.إ',  // UAE Dirham
    'SAR': '﷼',    // Saudi Riyal
    'KWD': 'KD',   // Kuwaiti Dinar
    'BHD': 'BD',   // Bahraini Dinar
    'QAR': 'QR',   // Qatari Rial
  };

  // Use Intl.NumberFormat for formatting the number part
  const formatter = new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

  // Format the amount and add the appropriate currency symbol
  const formattedAmount = formatter.format(amount);
  const symbol = currencySymbols[currency.toUpperCase()] || currency;

  // Special handling for JPY (Japanese Yen) since it typically has no decimal places
  if (currency.toUpperCase() === 'JPY') {
    const formatterWithoutDecimals = new Intl.NumberFormat('en-US', {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    });
    const formattedAmountWithoutDecimals = formatterWithoutDecimals.format(amount);
    return `${symbol}${formattedAmountWithoutDecimals}`;
  }

  return `${symbol}${formattedAmount}`;
}

export function mdToSafeHtml(md: string): string {
  const raw = marked.parse(md) as string;
  return DOMPurify.sanitize(raw);
}
