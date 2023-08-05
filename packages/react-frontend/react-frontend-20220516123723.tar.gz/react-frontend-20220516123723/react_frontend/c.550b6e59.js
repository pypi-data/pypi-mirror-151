import{_ as e,s as a,e as t,$ as i,u as l,f as o,ar as d,n}from"./main-ac83c92b.js";import{r}from"./c.3e14cfd3.js";import{t as s}from"./c.027db416.js";import"./c.25e73c3c.js";const u=()=>import("./c.d3bfdb7e.js");e([n("ha-date-input")],(function(e,a){return{F:class extends a{constructor(...a){super(...a),e(this)}},d:[{kind:"field",decorators:[t({attribute:!1})],key:"locale",value:void 0},{kind:"field",decorators:[t()],key:"value",value:void 0},{kind:"field",decorators:[t({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[t({type:Boolean})],key:"required",value:()=>!1},{kind:"field",decorators:[t()],key:"label",value:void 0},{kind:"field",decorators:[t()],key:"helper",value:void 0},{kind:"method",key:"render",value:function(){return i`<ha-textfield
      .label=${this.label}
      .helper=${this.helper}
      .disabled=${this.disabled}
      iconTrailing
      helperPersistent
      @click=${this._openDialog}
      .value=${this.value?r(new Date(this.value),this.locale):""}
      .required=${this.required}
    >
      <ha-svg-icon slot="trailingIcon" .path=${l}></ha-svg-icon>
    </ha-textfield>`}},{kind:"method",key:"_openDialog",value:function(){var e,a;this.disabled||(e=this,a={min:"1970-01-01",value:this.value,onChange:e=>this._valueChanged(e),locale:this.locale.language},o(e,"show-dialog",{dialogTag:"ha-dialog-date-picker",dialogImport:u,dialogParams:a}))}},{kind:"method",key:"_valueChanged",value:function(e){this.value!==e&&(this.value=e,o(this,"change"),o(this,"value-changed",{value:e}))}},{kind:"get",static:!0,key:"styles",value:function(){return d`
      ha-svg-icon {
        color: var(--secondary-text-color);
      }
    `}}]}}),a),e([n("ha-time-input")],(function(e,a){return{F:class extends a{constructor(...a){super(...a),e(this)}},d:[{kind:"field",decorators:[t({attribute:!1})],key:"locale",value:void 0},{kind:"field",decorators:[t()],key:"value",value:void 0},{kind:"field",decorators:[t()],key:"label",value:void 0},{kind:"field",decorators:[t()],key:"helper",value:void 0},{kind:"field",decorators:[t({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[t({type:Boolean})],key:"required",value:()=>!1},{kind:"field",decorators:[t({type:Boolean,attribute:"enable-second"})],key:"enableSecond",value:()=>!1},{kind:"method",key:"render",value:function(){var e;const a=s(this.locale),t=(null===(e=this.value)||void 0===e?void 0:e.split(":"))||[];let l=t[0];const o=Number(t[0]);return o&&a&&o>12&&o<24&&(l=String(o-12).padStart(2,"0")),a&&0===o&&(l="12"),i`
      <ha-base-time-input
        .label=${this.label}
        .hours=${Number(l)}
        .minutes=${Number(t[1])}
        .seconds=${Number(t[2])}
        .format=${a?12:24}
        .amPm=${a&&(o>=12?"PM":"AM")}
        .disabled=${this.disabled}
        @value-changed=${this._timeChanged}
        .enableSecond=${this.enableSecond}
        .required=${this.required}
        .helper=${this.helper}
      ></ha-base-time-input>
    `}},{kind:"method",key:"_timeChanged",value:function(e){e.stopPropagation();const a=e.detail.value,t=s(this.locale);let i=a.hours||0;a&&t&&("PM"===a.amPm&&i<12&&(i+=12),"AM"===a.amPm&&12===i&&(i=0));const l=`${i.toString().padStart(2,"0")}:${a.minutes?a.minutes.toString().padStart(2,"0"):"00"}:${a.seconds?a.seconds.toString().padStart(2,"0"):"00"}`;l!==this.value&&(this.value=l,o(this,"change"),o(this,"value-changed",{value:l}))}}]}}),a);
