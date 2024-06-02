export const initialActiveStrategies = {
  first: (items) => items[0] || console.error("No first item found"),
  last: (items) =>
    items[items.length - 1] || console.error("No last item found"),
  none: (items) => null,
  random: (items) =>
    items[Math.floor(Math.random() * items.length)] ||
    console.error("No random item found"),
};
// Dynamically generate strategies for specific indices
for (let i = 1; i <= 100; i++) {
  initialActiveStrategies[i] = (items) =>
    items[i - 1] || console.error(`No button at index ${i} found`);
  // TODO: add strategy to search for button by text content
}
