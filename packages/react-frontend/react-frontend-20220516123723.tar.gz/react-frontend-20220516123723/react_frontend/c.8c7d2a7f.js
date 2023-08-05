import{_ as i,s as e,t as r,$ as t,ar as o,n}from"./main-ac83c92b.js";i([n("hui-section-row")],(function(i,e){return{F:class extends e{constructor(...e){super(...e),i(this)}},d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[r()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(i){if(!i)throw new Error("Invalid configuration");this._config=i}},{kind:"method",key:"render",value:function(){return this._config?t`
      <div class="divider"></div>
      ${this._config.label?t`
            <div class="label" .title=${this._config.label}>
              ${this._config.label}
            </div>
          `:t``}
    `:t``}},{kind:"get",static:!0,key:"styles",value:function(){return o`
      .label {
        color: var(--section-header-text-color, var(--primary-text-color));
        margin-left: 8px;
        margin-bottom: 8px;
        margin-top: 16px;
        font-weight: 500;
      }
      .divider {
        height: 1px;
        background-color: var(--entities-divider-color, var(--divider-color));
        margin-left: -16px;
        margin-right: -16px;
        margin-top: 8px;
      }
    `}}]}}),e);
