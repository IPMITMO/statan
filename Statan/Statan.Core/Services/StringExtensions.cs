namespace Statan.Core.Services
{
    public static class StringExtensions
    {
        /// <summary>
        /// Truncates a start of string to the specified length with three dots in front.
        /// </summary>
        /// <param name="value">The value.</param>
        /// <param name="length">The length.</param>
        /// <returns>The short string.</returns>
        public static string Truncate(this string value, int length)
        {
            if (string.IsNullOrEmpty(value))
            {
                return value;
            }

            return value.Length <= length 
                ? value 
                : $"...{value.Substring(value.Length-length, length)}";
        }
    }
}
