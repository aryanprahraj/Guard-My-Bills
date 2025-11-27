export function formatCurrency(amount: number, currency: string = 'USD'): string {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency }).format(amount);
}

export function formatDate(date: string): string {
  return new Date(date).toLocaleDateString();
}

export function formatTime(time: string): string {
  return time;
}
