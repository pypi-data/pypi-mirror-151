import{_ as e,s as t,e as i,t as s,g as o,i as a,$ as n,dk as r,dl as d,ar as l,n as c}from"./main-ac83c92b.js";import{b6 as h,aW as u,aX as p,aV as _,aZ as k}from"./c.3e14cfd3.js";import{g as y,s as m,a as v}from"./c.9e1e758b.js";import{S as f}from"./c.02ed471c.js";import{r as b,b as g,s as D,e as w,d as x}from"./c.d4761680.js";import{g as $,f as j,s as z,d as C,c as S,a as T,b as K,i as O,e as P,h as V}from"./c.09ce6999.js";import"./c.027db416.js";import"./c.8cbd7110.js";import"./c.85c615ca.js";import"./c.40d6516d.js";e([c("hui-energy-period-selector")],(function(e,t){class c extends t{constructor(...t){super(...t),e(this)}}return{F:c,d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"collectionKey",value:void 0},{kind:"field",decorators:[s()],key:"_startDate",value:void 0},{kind:"field",decorators:[s()],key:"_endDate",value:void 0},{kind:"field",decorators:[s()],key:"_period",value:void 0},{kind:"method",key:"connectedCallback",value:function(){o(a(c.prototype),"connectedCallback",this).call(this),h(this,"narrow",this.offsetWidth<600)}},{kind:"method",key:"hassSubscribe",value:function(){return[y(this.hass,{key:this.collectionKey}).subscribe((e=>this._updateDates(e)))]}},{kind:"method",key:"render",value:function(){if(!this.hass||!this._startDate)return n``;const e=[{label:this.hass.localize("ui.panel.lovelace.components.energy_period_selector.day"),value:"day"},{label:this.hass.localize("ui.panel.lovelace.components.energy_period_selector.week"),value:"week"},{label:this.hass.localize("ui.panel.lovelace.components.energy_period_selector.month"),value:"month"},{label:this.hass.localize("ui.panel.lovelace.components.energy_period_selector.year"),value:"year"}];return n`
      <div class="row">
        <div class="label">
          ${"day"===this._period?u(this._startDate,this.hass.locale):"month"===this._period?p(this._startDate,this.hass.locale):"year"===this._period?_(this._startDate,this.hass.locale):`${k(this._startDate,this.hass.locale)} – ${k(this._endDate||new Date,this.hass.locale)}`}
          <ha-icon-button
            .label=${this.hass.localize("ui.panel.lovelace.components.energy_period_selector.previous")}
            @click=${this._pickPrevious}
            .path=${r}
          ></ha-icon-button>
          <ha-icon-button
            .label=${this.hass.localize("ui.panel.lovelace.components.energy_period_selector.next")}
            @click=${this._pickNext}
            .path=${d}
          ></ha-icon-button>
          <mwc-button dense outlined @click=${this._pickToday}>
            ${this.hass.localize("ui.panel.lovelace.components.energy_period_selector.today")}
          </mwc-button>
        </div>
        <div class="period">
          <ha-button-toggle-group
            .buttons=${e}
            .active=${this._period}
            dense
            @value-changed=${this._handleView}
          ></ha-button-toggle-group>
        </div>
      </div>
    `}},{kind:"method",key:"_handleView",value:function(e){this._period=e.detail.value;const t=m(),i=!this._startDate||function(e,t){b(2,arguments);var i=g(e).getTime(),s=g(t.start).getTime(),o=g(t.end).getTime();if(!(s<=o))throw new RangeError("Invalid interval");return i>=s&&i<=o}(t,{start:this._startDate,end:this._endDate||v()})?t:this._startDate;this._setDate("day"===this._period?D(i):"week"===this._period?$(i,{weekStartsOn:1}):"month"===this._period?j(i):z(i))}},{kind:"method",key:"_pickToday",value:function(){this._setDate("day"===this._period?m():"week"===this._period?$(new Date,{weekStartsOn:1}):"month"===this._period?j(new Date):z(new Date))}},{kind:"method",key:"_pickPrevious",value:function(){const e="day"===this._period?C(this._startDate,-1):"week"===this._period?S(this._startDate,-1):"month"===this._period?T(this._startDate,-1):K(this._startDate,-1);this._setDate(e)}},{kind:"method",key:"_pickNext",value:function(){const e="day"===this._period?C(this._startDate,1):"week"===this._period?S(this._startDate,1):"month"===this._period?T(this._startDate,1):K(this._startDate,1);this._setDate(e)}},{kind:"method",key:"_setDate",value:function(e){const t="day"===this._period?w(e):"week"===this._period?O(e,{weekStartsOn:1}):"month"===this._period?P(e):V(e),i=y(this.hass,{key:this.collectionKey});i.setPeriod(e,t),i.refresh()}},{kind:"method",key:"_updateDates",value:function(e){this._startDate=e.start,this._endDate=e.end||v();const t=x(this._endDate,this._startDate);this._period=t<1?"day":6===t?"week":t>26&&t<31?"month":364===t||365===t?"year":void 0}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      .row {
        display: flex;
        justify-content: flex-end;
      }
      :host([narrow]) .row {
        flex-direction: column-reverse;
      }
      :host([narrow]) .period {
        margin-bottom: 8px;
      }
      .label {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        font-size: 20px;
      }
      .period {
        display: flex;
        justify-content: flex-end;
      }
      :host {
        --mdc-button-outline-color: currentColor;
        --primary-color: currentColor;
        --mdc-theme-primary: currentColor;
        --mdc-button-disabled-outline-color: var(--disabled-text-color);
        --mdc-button-disabled-ink-color: var(--disabled-text-color);
        --mdc-icon-button-ripple-opacity: 0.2;
      }
      ha-icon-button {
        --mdc-icon-button-size: 28px;
      }
      ha-button-toggle-group {
        padding-left: 8px;
      }
      mwc-button {
        flex-shrink: 0;
      }
    `}}]}}),f(t));let F=e([c("hui-energy-date-selection-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s()],key:"_config",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 1}},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"method",key:"render",value:function(){return this.hass&&this._config?n`
      <hui-energy-period-selector
        .hass=${this.hass}
        .collectionKey=${this._config.collection_key}
      ></hui-energy-period-selector>
    `:n``}},{kind:"get",static:!0,key:"styles",value:function(){return l``}}]}}),t);export{F as HuiEnergyDateSelectionCard};
