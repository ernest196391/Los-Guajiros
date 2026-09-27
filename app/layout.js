import "./globals.css";
import InstallPrompt from "./InstallPrompt";
import {tenant} from "../lib/tenant";
import {Fraunces,Nunito_Sans} from "next/font/google";

const displayFont=Fraunces({subsets:["latin"],variable:"--font-display",display:"swap"});
const bodyFont=Nunito_Sans({subsets:["latin"],variable:"--font-body",display:"swap"});
const themeVars=Object.entries({"--ink":tenant.theme.ink,"--deep":tenant.theme.primary,"--orange":tenant.theme.accent,"--mint":tenant.theme.mint,"--assistant-teal":tenant.theme.assistant,"--assistant-dark":tenant.theme.assistantDark,"--assistant-brand":tenant.theme.assistantInk,"--assistant-border":tenant.theme.assistantBorder,"--assistant-tint":tenant.theme.assistantSoft,"--assistant-tint-hover":tenant.theme.assistantSoftHover}).map(([k,v])=>k+":"+v).join(";");
export const metadata={
  title:tenant.seo.title,
  description:tenant.seo.description,
  manifest:"/manifest.webmanifest",
  icons:{
    icon:[
      {url:"/favicon.svg",type:"image/svg+xml"}
    ],
    apple:"/apple-touch-icon.png?v=4"
  },
  appleWebApp:{capable:true,title:tenant.shortName,statusBarStyle:"default"},
  robots:{index:true,follow:true},
  openGraph:{title:tenant.seo.title,description:tenant.seo.description,type:"website",locale:"es_CU"}
};
export const viewport={themeColor:tenant.theme.assistant,width:"device-width",initialScale:1};
export default function RootLayout({children}){return <html lang="es" className={`${displayFont.variable} ${bodyFont.variable}`}><body><style dangerouslySetInnerHTML={{__html:":root,.assistantV2{"+themeVars+"}"}}/>{children}<InstallPrompt/></body></html>}
