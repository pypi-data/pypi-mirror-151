import{_ as e,s as t,e as i,$ as a,ar as s,f as l,n as d}from"./main-ac83c92b.js";import{s as r}from"./c.027db416.js";import"./c.3e14cfd3.js";e([d("ha-theme-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:()=>!1},{kind:"method",key:"render",value:function(){return a`
      <ha-select
        .label=${this.label||this.hass.localize("ui.components.theme_picker.theme")}
        .value=${this.value}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${r}
        fixedMenuPosition
        naturalMenuWidth
      >
        <mwc-list-item value="remove"
          >${this.hass.localize("ui.components.theme_picker.no_theme")}</mwc-list-item
        >
        ${Object.keys(this.hass.themes.themes).sort().map((e=>a`<mwc-list-item .value=${e}>${e}</mwc-list-item>`))}
      </ha-select>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return s`
      ha-select {
        width: 100%;
      }
    `}},{kind:"method",key:"_changed",value:function(e){this.hass&&""!==e.target.value&&(this.value="remove"===e.target.value?void 0:e.target.value,l(this,"value-changed",{value:this.value}))}}]}}),t);
