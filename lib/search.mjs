export const normalizeSearch=text=>String(text||"")
  .normalize("NFD")
  .replace(/[\u0300-\u036f]/g,"")
  .toLowerCase()
  .trim();

export function searchProducts(products,query,category="Todos"){
  const terms=normalizeSearch(query).split(/\s+/).filter(Boolean);
  return products
    .filter(product=>{
      if(!terms.length&&category!=="Todos"&&product.c!==category)return false;
      const fields=[product.n,product.c,product.d].map(normalizeSearch);
      return terms.every(term=>fields.some(field=>field.includes(term)));
    })
    .sort((a,b)=>{
      if(!terms.length)return 0;
      const term=normalizeSearch(query),aName=normalizeSearch(a.n),bName=normalizeSearch(b.n);
      const score=name=>name===term?0:name.startsWith(term)?1:name.includes(term)?2:3;
      return score(aName)-score(bName);
    });
}
