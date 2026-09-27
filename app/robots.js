import {tenant} from "../lib/tenant";

export default function robots(){
  return {
    rules:{userAgent:"*",allow:"/",disallow:["/api/"]},
    sitemap:`${tenant.url}/sitemap.xml`,
    host:tenant.url
  };
}
