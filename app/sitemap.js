import {tenant} from "../lib/tenant";

export default function sitemap(){
  return [
    {url:`${tenant.url}/`,lastModified:new Date(),changeFrequency:"daily",priority:1},
    {url:`${tenant.url}/checkout`,lastModified:new Date(),changeFrequency:"weekly",priority:.5}
  ];
}
