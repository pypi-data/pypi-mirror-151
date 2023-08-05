import{_ as e,s as r,t as i,$ as t,ar as o,n}from"./main-ac83c92b.js";import{d as c}from"./c.d6711a1d.js";import"./c.3e14cfd3.js";import"./c.027db416.js";import"./c.8cbd7110.js";let s=e([n("hui-error-card")],(function(e,r){return{F:class extends r{constructor(...r){super(...r),e(this)}},d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"_config",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 4}},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"method",key:"render",value:function(){if(!this._config)return t``;let e;if(this._config.origConfig)try{e=c(this._config.origConfig)}catch(r){e=`[Error dumping ${this._config.origConfig}]`}return t`<ha-alert alert-type="error" .title=${this._config.error}>
      ${e?t`<pre>${e}</pre>`:""}
    </ha-alert>`}},{kind:"get",static:!0,key:"styles",value:function(){return o`
      pre {
        font-family: var(--code-font-family, monospace);
        white-space: break-spaces;
        user-select: text;
      }
    `}}]}}),r);export{s as HuiErrorCard};
