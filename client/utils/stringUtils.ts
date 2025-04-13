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
 * Extracts first name from a full name
 */
export function getFirstName(fullName: string): string {
  if (!fullName) return '';
  return fullName.split(' ')[0];
}
