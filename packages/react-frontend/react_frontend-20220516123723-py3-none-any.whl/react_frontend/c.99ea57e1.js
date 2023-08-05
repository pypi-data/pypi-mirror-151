import{_ as e,s as i,e as a,t,m as s,$ as c,f as o,ar as l,n}from"./main-ac83c92b.js";import"./c.3fc42334.js";import"./c.1fca9ca6.js";import{X as r,Y as d,Z as h,a1 as m,_ as u,$ as f,a2 as p,a0 as v}from"./c.3e14cfd3.js";import{b as g}from"./c.461e571b.js";import"./c.53212acc.js";import"./c.027db416.js";import"./c.cfa85e17.js";import"./c.0e001851.js";import"./c.4e93087d.js";import"./c.8eddd911.js";import"./c.c8193d47.js";import"./c.47fa9be3.js";import"./c.e9aa747b.js";import"./c.8e198788.js";import"./c.25e73c3c.js";import"./c.5ea5eadd.js";import"./c.8cbd7110.js";const k=r(g,d({title:h(m([u(),f()])),initial_view:h(u()),theme:h(u()),entities:p(u())})),_=["dayGridMonth","dayGridDay","listWeek"];let j=e([n("hui-calendar-card-editor")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[t()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(e){v(e,k),this._config=e}},{kind:"field",key:"_schema",value:()=>s((e=>[{name:"",type:"grid",schema:[{name:"title",required:!1,selector:{text:{}}},{name:"initial_view",required:!1,selector:{select:{options:_.map((i=>[i,e(`ui.panel.lovelace.editor.card.calendar.views.${i}`)]))}}}]},{name:"theme",required:!1,selector:{theme:{}}}]))},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return c``;const e=this._schema(this.hass.localize),i={initial_view:"dayGridMonth",...this._config};return c`
      <ha-form
        .hass=${this.hass}
        .data=${i}
        .schema=${e}
        .computeLabel=${this._computeLabelCallback}
        @value-changed=${this._valueChanged}
      ></ha-form>
      <h3>
        ${this.hass.localize("ui.panel.lovelace.editor.card.calendar.calendar_entities")+" ("+this.hass.localize("ui.panel.lovelace.editor.card.config.required")+")"}
      </h3>
      <ha-entities-picker
        .hass=${this.hass}
        .value=${this._config.entities}
        .includeDomains=${["calendar"]}
        @value-changed=${this._entitiesChanged}
      >
      </ha-entities-picker>
    `}},{kind:"method",key:"_valueChanged",value:function(e){const i=e.detail.value;o(this,"config-changed",{config:i})}},{kind:"method",key:"_entitiesChanged",value:function(e){const i={...this._config,entities:e.detail.value};o(this,"config-changed",{config:i})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>"title"===e.name?this.hass.localize("ui.panel.lovelace.editor.card.generic.title"):"theme"===e.name?`${this.hass.localize("ui.panel.lovelace.editor.card.generic.theme")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})`:this.hass.localize(`ui.panel.lovelace.editor.card.calendar.${e.name}`)}},{kind:"field",static:!0,key:"styles",value:()=>l`
    ha-form {
      display: block;
      overflow: auto;
    }
  `}]}}),i);export{j as HuiCalendarCardEditor};
