// Emitted by tools/build.py from the validated pricing record; never shipped.
declare module '*pricing-data.js' {
  const pricing: {
    bases: {id: string; name: string; group: string; price: number}[];
    options: {id: string; name: string; group: string; price: number; kind: string}[];
  };
  export default pricing;
}

declare module '*project-links.js' {
 const links: Readonly<Record<string, string>>;
 export default links;
}
