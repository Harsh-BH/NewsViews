/**
 * Masks a phone number, showing only first 3 and last 2 digits
 * Example: "9876543210" becomes "987****10"
 */
export function maskPhoneNumber(phoneNumber: string): string {
  if (!phoneNumber || phoneNumber.length < 5) return phoneNumber;
  
  const firstPart = phoneNumber.substring(0, 3);
  const lastPart = phoneNumber.substring(phoneNumber.length - 2);
  const maskedPart = '*'.repeat(4);
  
  return `${firstPart}${maskedPart}${lastPart}`;
}

/**
 * Extracts the first name from a full name string
 * @param name The full name to process
 * @returns The first name
 */
export function getFirstName(name?: string): string {
  if (!name) return 'User';
  
  const trimmedName = name.trim();
  if (trimmedName.length === 0) return 'User';
  
  // Get first part of name before any space
  return trimmedName.split(' ')[0];
}
