import{_ as e,$ as s,g as a,i as c,f as t,n as o}from"./main-ac83c92b.js";import{X as i,Y as r,a2 as m,a6 as n,Z as d,_ as p,$ as l,a7 as u,a0 as h}from"./c.3e14cfd3.js";import{b as f}from"./c.461e571b.js";import{HuiStackCardEditor as j}from"./c.20687dc8.js";import"./c.027db416.js";import"./c.8cbd7110.js";import"./c.904ea19c.js";import"./c.213328e9.js";import"./c.d6711a1d.js";import"./c.c018532e.js";import"./c.622dfac1.js";import"./c.1fca9ca6.js";import"./c.4e93087d.js";import"./c.8eddd911.js";import"./c.c8193d47.js";import"./c.47fa9be3.js";import"./c.e9aa747b.js";import"./c.8e198788.js";import"./c.25e73c3c.js";import"./c.5ea5eadd.js";import"./c.60f8b094.js";import"./c.1430be7b.js";import"./c.f5888e17.js";import"./c.0660f3f3.js";import"./c.ad12eed4.js";const b=i(f,r({cards:m(n()),title:d(p()),square:d(l()),columns:d(u())})),g=[{type:"grid",name:"",schema:[{name:"columns",selector:{number:{min:1,mode:"box"}}},{name:"square",selector:{boolean:{}}}]}];let k=e([o("hui-grid-card-editor")],(function(e,o){class i extends o{constructor(...s){super(...s),e(this)}}return{F:i,d:[{kind:"method",key:"setConfig",value:function(e){h(e,b),this._config=e}},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return s``;const e={square:!0,columns:3,...this._config};return s`
      <ha-form
        .hass=${this.hass}
        .data=${e}
        .schema=${g}
        .computeLabel=${this._computeLabelCallback}
        @value-changed=${this._valueChanged}
      ></ha-form>
      ${a(c(i.prototype),"render",this).call(this)}
    `}},{kind:"method",key:"_valueChanged",value:function(e){t(this,"config-changed",{config:e.detail.value})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.panel.lovelace.editor.card.grid.${e.name}`)}}]}}),j);export{k as HuiGridCardEditor};
