export const normalizeSearch=text=>String(text||"")
  .normalize("NFD")
  .replace(/[\u0300-\u036f]/g,"")
  .toLowerCase()
  .trim();

function distance(a,b){
  if(a===b)return 0;
  if(!a.length)return b.length;
  if(!b.length)return a.length;
  const previous=Array.from({length:b.length+1},(_,index)=>index);
  for(let i=1;i<=a.length;i++){
    let diagonal=previous[0];
    previous[0]=i;
    for(let j=1;j<=b.length;j++){
      const above=previous[j],cost=a[i-1]===b[j-1]?0:1;
      previous[j]=Math.min(previous[j]+1,previous[j-1]+1,diagonal+cost);
      diagonal=above;
    }
  }
  return previous[b.length];
}

function termScore(term,fields){
  const words=fields.flatMap(field=>field.split(/[^a-z0-9ñ]+/).filter(Boolean));
  if(words.some(word=>word===term))return 0;
  if(words.some(word=>word.startsWith(term)))return 1;
  if(fields.some(field=>field.includes(term)))return 2;
  const tolerance=term.length>=6?2:term.length>=4?1:0;
  if(tolerance&&words.some(word=>Math.abs(word.length-term.length)<=tolerance&&distance(word,term)<=tolerance))return 3;
  return Number.POSITIVE_INFINITY;
}

export function searchProducts(products,query,category="Todos"){
  const terms=normalizeSearch(query).split(/\s+/).filter(Boolean);
  return products
    .map((product,index)=>{
      const fields=[product.n,product.c,product.d].map(normalizeSearch);
      const scores=terms.map(term=>termScore(term,fields));
      return {product,index,score:scores.reduce((sum,value)=>sum+value,0),matches:scores.every(Number.isFinite)};
    })
    .filter(result=>terms.length?result.matches:category==="Todos"||result.product.c===category)
    .sort((a,b)=>a.score-b.score||a.index-b.index)
    .map(result=>result.product);
}
