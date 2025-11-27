export function isValidAmount(amount: any): boolean {
  return typeof amount === 'number' && !isNaN(amount) && amount >= 0;
}

export function isValidDate(date: string): boolean {
  return !isNaN(Date.parse(date));
}

export function isValidTime(time: string): boolean {
  // Simple check for HH:MM:SS
  return /^\d{2}:\d{2}:\d{2}$/.test(time);
}
