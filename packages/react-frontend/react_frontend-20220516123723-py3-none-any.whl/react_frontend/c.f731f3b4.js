import{_ as e,cK as o,e as t,g as n,i as r,f as a,n as i,s as d,$ as s,ar as l}from"./main-ac83c92b.js";import{w as c}from"./c.d2605417.js";import"./c.3e14cfd3.js";let k;e([i("ha-markdown-element")],(function(e,o){class i extends o{constructor(...o){super(...o),e(this)}}return{F:i,d:[{kind:"field",decorators:[t()],key:"content",value:void 0},{kind:"field",decorators:[t({type:Boolean})],key:"allowSvg",value:()=>!1},{kind:"field",decorators:[t({type:Boolean})],key:"breaks",value:()=>!1},{kind:"method",key:"createRenderRoot",value:function(){return this}},{kind:"method",key:"update",value:function(e){n(r(i.prototype),"update",this).call(this,e),void 0!==this.content&&this._render()}},{kind:"method",key:"_render",value:async function(){this.innerHTML=await(async(e,o,t)=>(k||(k=c(new Worker(new URL("./markdown_worker",import.meta.url)))),k.renderMarkdown(e,o,t)))(String(this.content),{breaks:this.breaks,gfm:!0},{allowSvg:this.allowSvg}),this._resize();const e=document.createTreeWalker(this,NodeFilter.SHOW_ELEMENT,null);for(;e.nextNode();){const o=e.currentNode;o instanceof HTMLAnchorElement&&o.host!==document.location.host?(o.target="_blank",o.rel="noreferrer noopener"):o instanceof HTMLImageElement&&o.addEventListener("load",this._resize)}}},{kind:"field",key:"_resize",value(){return()=>a(this,"iron-resize")}}]}}),o),e([i("ha-markdown")],(function(e,o){return{F:class extends o{constructor(...o){super(...o),e(this)}},d:[{kind:"field",decorators:[t()],key:"content",value:void 0},{kind:"field",decorators:[t({type:Boolean})],key:"allowSvg",value:()=>!1},{kind:"field",decorators:[t({type:Boolean})],key:"breaks",value:()=>!1},{kind:"method",key:"render",value:function(){return this.content?s`<ha-markdown-element
      .content=${this.content}
      .allowSvg=${this.allowSvg}
      .breaks=${this.breaks}
    ></ha-markdown-element>`:s``}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      :host {
        display: block;
      }
      ha-markdown-element {
        -ms-user-select: text;
        -webkit-user-select: text;
        -moz-user-select: text;
      }
      ha-markdown-element > *:first-child {
        margin-top: 0;
      }
      ha-markdown-element > *:last-child {
        margin-bottom: 0;
      }
      a {
        color: var(--primary-color);
      }
      img {
        max-width: 100%;
      }
      code,
      pre {
        background-color: var(--markdown-code-background-color, none);
        border-radius: 3px;
      }
      svg {
        background-color: var(--markdown-svg-background-color, none);
        color: var(--markdown-svg-color, none);
      }
      code {
        font-size: 85%;
        padding: 0.2em 0.4em;
      }
      pre code {
        padding: 0;
      }
      pre {
        padding: 16px;
        overflow: auto;
        line-height: 1.45;
        font-family: var(--code-font-family, monospace);
      }
      h1,
      h2,
      h3,
      h4,
      h5,
      h6 {
        line-height: initial;
      }
      h2 {
        font-size: 1.5em;
        font-weight: bold;
      }
    `}}]}}),d);
