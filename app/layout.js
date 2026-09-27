import "./globals.css";
import InstallPrompt from "./InstallPrompt";
import {tenant} from "../lib/tenant";
import {products} from "../lib/catalog";
import {Fraunces,Nunito_Sans} from "next/font/google";

const displayFont=Fraunces({subsets:["latin"],variable:"--font-display",display:"swap"});
const bodyFont=Nunito_Sans({subsets:["latin"],variable:"--font-body",display:"swap"});
const siteUrl=tenant.url;
const themeVars=Object.entries({"--ink":tenant.theme.ink,"--deep":tenant.theme.primary,"--orange":tenant.theme.accent,"--mint":tenant.theme.mint,"--assistant-teal":tenant.theme.assistant,"--assistant-dark":tenant.theme.assistantDark,"--assistant-brand":tenant.theme.assistantInk,"--assistant-border":tenant.theme.assistantBorder,"--assistant-tint":tenant.theme.assistantSoft,"--assistant-tint-hover":tenant.theme.assistantSoftHover}).map(([k,v])=>k+":"+v).join(";");
export const metadata={
  metadataBase:new URL(siteUrl),
  title:tenant.seo.title,
  description:tenant.seo.description,
  applicationName:tenant.name,
  keywords:[tenant.name,"comida casera en Marianao","jugos en Marianao","natillas","meriendas","mensajería en Marianao"],
  alternates:{canonical:"/"},
  manifest:"/manifest.webmanifest",
  icons:{
    icon:[
      {url:"/favicon.svg",type:"image/svg+xml"}
    ],
    apple:"/apple-touch-icon.png?v=4"
  },
  appleWebApp:{capable:true,title:tenant.shortName,statusBarStyle:"default"},
  robots:{index:true,follow:true,googleBot:{index:true,follow:true,"max-image-preview":"large","max-snippet":-1,"max-video-preview":-1}},
  openGraph:{title:tenant.seo.title,description:tenant.seo.description,url:siteUrl,siteName:tenant.name,type:"website",locale:"es_CU",images:[{url:"/brand/fachada-hero-dia.webp",width:1672,height:941,alt:tenant.hero.alt}]},
  twitter:{card:"summary_large_image",title:tenant.seo.title,description:tenant.seo.description,images:["/brand/fachada-hero-dia.webp"]}
};
export const viewport={themeColor:tenant.theme.assistant,width:"device-width",initialScale:1};
const structuredData={"@context":"https://schema.org","@type":"FoodEstablishment",name:tenant.name,url:siteUrl,image:`${siteUrl}/brand/fachada-hero-dia.webp`,logo:`${siteUrl}/brand/logo.svg`,description:tenant.seo.description,telephone:`+${tenant.whatsapp}`,priceRange:"$",currenciesAccepted:tenant.currency,address:{"@type":"PostalAddress",streetAddress:"Calle 88",addressLocality:"Marianao",addressRegion:"La Habana",addressCountry:"CU"},areaServed:{"@type":"AdministrativeArea",name:"Marianao, La Habana"},openingHoursSpecification:[{"@type":"OpeningHoursSpecification",dayOfWeek:["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],opens:"09:00",closes:"21:00"}],hasMenu:{"@type":"Menu",name:`Catálogo de ${tenant.name}`,hasMenuSection:[...new Set(products.map(p=>p.c))].map(category=>({"@type":"MenuSection",name:category,hasMenuItem:products.filter(p=>p.c===category).map(p=>({"@type":"MenuItem",name:p.n,description:p.d,image:`${siteUrl}${p.img}`,offers:{"@type":"Offer",price:p.p,priceCurrency:tenant.currency,availability:p.disabled?"https://schema.org/PreOrder":"https://schema.org/InStock",url:siteUrl}}))}))}};
export default function RootLayout({children}){return <html lang="es-CU" className={`${displayFont.variable} ${bodyFont.variable}`}><body><style dangerouslySetInnerHTML={{__html:":root,.assistantV2{"+themeVars+"}"}}/><script type="application/ld+json" dangerouslySetInnerHTML={{__html:JSON.stringify(structuredData).replace(/</g,"\\u003c")}}/>{children}<InstallPrompt/></body></html>}
