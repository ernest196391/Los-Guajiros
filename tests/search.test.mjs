import test from "node:test";
import assert from "node:assert/strict";
import {products} from "../lib/catalog.js";
import {searchProducts} from "../lib/search.mjs";

test("search ignores accents and case",()=>{
  assert.equal(searchProducts(products,"COCTEL")[0].n,"Cóctel de frutas");
});

test("search escapes a previously selected category",()=>{
  assert.equal(searchProducts(products,"jugo","Ensaladas")[0].n,"Jugo de guayaba");
});

test("multiword search checks product fields",()=>{
  assert.equal(searchProducts(products,"natilla coco")[0].n,"Natilla de coco");
});

test("empty search still respects selected category",()=>{
  assert.ok(searchProducts(products,"","Comida casera").every(product=>product.c==="Comida casera"));
});

test("search suggests products despite a typing mistake",()=>{
  assert.equal(searchProducts(products,"guayva")[0].n,"Jugo de guayaba");
});

test("exact product name ranks before description matches",()=>{
  assert.equal(searchProducts(products,"ensalada")[0].n,"Ensalada fría");
});
