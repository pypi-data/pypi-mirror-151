import{_ as e,s as t,e as a,t as c,$ as r,ez as o,eA as d,eh as l,eB as i,eg as n,eC as s,aA as m,ar as b,cJ as _,n as h}from"./main-ac83c92b.js";import{c as p}from"./c.027db416.js";import{b8 as g,Q as u}from"./c.3e14cfd3.js";import"./c.b57a34a6.js";import{g as f,e as k,b as x}from"./c.9e1e758b.js";import{S as y}from"./c.02ed471c.js";import"./c.8cbd7110.js";import"./c.85c615ca.js";import"./c.40d6516d.js";import"./c.d4761680.js";let v=e([h("hui-energy-sources-table-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[c()],key:"_config",value:void 0},{kind:"field",decorators:[c()],key:"_data",value:void 0},{kind:"field",key:"hassSubscribeRequiredHostProps",value:()=>["_config"]},{kind:"method",key:"hassSubscribe",value:function(){var e;return[f(this.hass,{key:null===(e=this._config)||void 0===e?void 0:e.collection_key}).subscribe((e=>{this._data=e}))]}},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"method",key:"render",value:function(){var e,t,a,c,b,_,h;if(!this.hass||!this._config)return r``;if(!this._data)return r`${this.hass.localize("ui.panel.lovelace.cards.energy.loading")}`;let f=0,y=0,v=0,w=0,$=0,z=0;const F=k(this._data.prefs),E=getComputedStyle(this),C=E.getPropertyValue("--energy-solar-color").trim(),Y=E.getPropertyValue("--energy-battery-out-color").trim(),X=E.getPropertyValue("--energy-battery-in-color").trim(),j=E.getPropertyValue("--energy-grid-return-color").trim(),R=E.getPropertyValue("--energy-grid-consumption-color").trim(),A=E.getPropertyValue("--energy-gas-color").trim(),M=(null===(e=F.grid)||void 0===e?void 0:e[0].flow_from.some((e=>e.stat_cost||e.entity_energy_price||e.number_energy_price)))||(null===(t=F.grid)||void 0===t?void 0:t[0].flow_to.some((e=>e.stat_compensation||e.entity_energy_price||e.number_energy_price)))||(null===(a=F.gas)||void 0===a?void 0:a.some((e=>e.stat_cost||e.entity_energy_price||e.number_energy_price))),S=x(this.hass,this._data.prefs)||"";return r` <ha-card>
      ${this._config.title?r`<h1 class="card-header">${this._config.title}</h1>`:""}
      <div class="mdc-data-table">
        <div class="mdc-data-table__table-container">
          <table class="mdc-data-table__table" aria-label="Energy sources">
            <thead>
              <tr class="mdc-data-table__header-row">
                <th class="mdc-data-table__header-cell"></th>
                <th
                  class="mdc-data-table__header-cell"
                  role="columnheader"
                  scope="col"
                >
                  ${this.hass.localize("ui.panel.lovelace.cards.energy.energy_sources_table.source")}
                </th>
                <th
                  class="mdc-data-table__header-cell mdc-data-table__header-cell--numeric"
                  role="columnheader"
                  scope="col"
                >
                  ${this.hass.localize("ui.panel.lovelace.cards.energy.energy_sources_table.energy")}
                </th>
                ${M?r` <th
                      class="mdc-data-table__header-cell mdc-data-table__header-cell--numeric"
                      role="columnheader"
                      scope="col"
                    >
                      ${this.hass.localize("ui.panel.lovelace.cards.energy.energy_sources_table.cost")}
                    </th>`:""}
              </tr>
            </thead>
            <tbody class="mdc-data-table__content">
              ${null===(c=F.solar)||void 0===c?void 0:c.map(((e,t)=>{const a=this.hass.states[e.stat_energy_from],c=g(this._data.stats[e.stat_energy_from])||0;v+=c;const b=t>0?this.hass.themes.darkMode?o(d(l(C)),t):i(d(l(C)),t):void 0,_=b?n(s(b)):C;return r`<tr class="mdc-data-table__row">
                  <td class="mdc-data-table__cell cell-bullet">
                    <div
                      class="bullet"
                      style=${m({borderColor:_,backgroundColor:_+"7F"})}
                    ></div>
                  </td>
                  <th class="mdc-data-table__cell" scope="row">
                    ${a?p(a):e.stat_energy_from}
                  </th>
                  <td
                    class="mdc-data-table__cell mdc-data-table__cell--numeric"
                  >
                    ${u(c,this.hass.locale)} kWh
                  </td>
                  ${M?r`<td class="mdc-data-table__cell"></td>`:""}
                </tr>`}))}
              ${F.solar?r`<tr class="mdc-data-table__row total">
                    <td class="mdc-data-table__cell"></td>
                    <th class="mdc-data-table__cell" scope="row">
                      Solar total
                    </th>
                    <td
                      class="mdc-data-table__cell mdc-data-table__cell--numeric"
                    >
                      ${u(v,this.hass.locale)} kWh
                    </td>
                    ${M?r`<td class="mdc-data-table__cell"></td>`:""}
                  </tr>`:""}
              ${null===(b=F.battery)||void 0===b?void 0:b.map(((e,t)=>{const a=this.hass.states[e.stat_energy_from],c=this.hass.states[e.stat_energy_to],b=g(this._data.stats[e.stat_energy_from])||0,_=g(this._data.stats[e.stat_energy_to])||0;w+=b-_;const h=t>0?this.hass.themes.darkMode?o(d(l(Y)),t):i(d(l(Y)),t):void 0,f=h?n(s(h)):Y,k=t>0?this.hass.themes.darkMode?o(d(l(X)),t):i(d(l(X)),t):void 0,x=k?n(s(k)):X;return r`<tr class="mdc-data-table__row">
                    <td class="mdc-data-table__cell cell-bullet">
                      <div
                        class="bullet"
                        style=${m({borderColor:f,backgroundColor:f+"7F"})}
                      ></div>
                    </td>
                    <th class="mdc-data-table__cell" scope="row">
                      ${a?p(a):e.stat_energy_from}
                    </th>
                    <td
                      class="mdc-data-table__cell mdc-data-table__cell--numeric"
                    >
                      ${u(b,this.hass.locale)} kWh
                    </td>
                    ${M?r`<td class="mdc-data-table__cell"></td>`:""}
                  </tr>
                  <tr class="mdc-data-table__row">
                    <td class="mdc-data-table__cell cell-bullet">
                      <div
                        class="bullet"
                        style=${m({borderColor:x,backgroundColor:x+"7F"})}
                      ></div>
                    </td>
                    <th class="mdc-data-table__cell" scope="row">
                      ${c?p(c):e.stat_energy_from}
                    </th>
                    <td
                      class="mdc-data-table__cell mdc-data-table__cell--numeric"
                    >
                      ${u(-1*_,this.hass.locale)} kWh
                    </td>
                    ${M?r`<td class="mdc-data-table__cell"></td>`:""}
                  </tr>`}))}
              ${F.battery?r`<tr class="mdc-data-table__row total">
                    <td class="mdc-data-table__cell"></td>
                    <th class="mdc-data-table__cell" scope="row">
                      ${this.hass.localize("ui.panel.lovelace.cards.energy.energy_sources_table.battery_total")}
                    </th>
                    <td
                      class="mdc-data-table__cell mdc-data-table__cell--numeric"
                    >
                      ${u(w,this.hass.locale)} kWh
                    </td>
                    ${M?r`<td class="mdc-data-table__cell"></td>`:""}
                  </tr>`:""}
              ${null===(_=F.grid)||void 0===_?void 0:_.map((e=>r`${e.flow_from.map(((e,t)=>{const a=this.hass.states[e.stat_energy_from],c=g(this._data.stats[e.stat_energy_from])||0;f+=c;const b=e.stat_cost||this._data.info.cost_sensors[e.stat_energy_from],_=b?g(this._data.stats[b])||0:null;null!==_&&(y+=_);const h=t>0?this.hass.themes.darkMode?o(d(l(R)),t):i(d(l(R)),t):void 0,k=h?n(s(h)):R;return r`<tr class="mdc-data-table__row">
                    <td class="mdc-data-table__cell cell-bullet">
                      <div
                        class="bullet"
                        style=${m({borderColor:k,backgroundColor:k+"7F"})}
                      ></div>
                    </td>
                    <th class="mdc-data-table__cell" scope="row">
                      ${a?p(a):e.stat_energy_from}
                    </th>
                    <td
                      class="mdc-data-table__cell mdc-data-table__cell--numeric"
                    >
                      ${u(c,this.hass.locale)} kWh
                    </td>
                    ${M?r` <td
                          class="mdc-data-table__cell mdc-data-table__cell--numeric"
                        >
                          ${null!==_?u(_,this.hass.locale,{style:"currency",currency:this.hass.config.currency}):""}
                        </td>`:""}
                  </tr>`}))}
                ${e.flow_to.map(((e,t)=>{const a=this.hass.states[e.stat_energy_to],c=-1*(g(this._data.stats[e.stat_energy_to])||0);f+=c;const b=e.stat_compensation||this._data.info.cost_sensors[e.stat_energy_to],_=b?-1*(g(this._data.stats[b])||0):null;null!==_&&(y+=_);const h=t>0?this.hass.themes.darkMode?o(d(l(j)),t):i(d(l(j)),t):void 0,k=h?n(s(h)):j;return r`<tr class="mdc-data-table__row">
                    <td class="mdc-data-table__cell cell-bullet">
                      <div
                        class="bullet"
                        style=${m({borderColor:k,backgroundColor:k+"7F"})}
                      ></div>
                    </td>
                    <th class="mdc-data-table__cell" scope="row">
                      ${a?p(a):e.stat_energy_to}
                    </th>
                    <td
                      class="mdc-data-table__cell mdc-data-table__cell--numeric"
                    >
                      ${u(c,this.hass.locale)} kWh
                    </td>
                    ${M?r` <td
                          class="mdc-data-table__cell mdc-data-table__cell--numeric"
                        >
                          ${null!==_?u(_,this.hass.locale,{style:"currency",currency:this.hass.config.currency}):""}
                        </td>`:""}
                  </tr>`}))}`))}
              ${F.grid?r` <tr class="mdc-data-table__row total">
                    <td class="mdc-data-table__cell"></td>
                    <th class="mdc-data-table__cell" scope="row">
                      ${this.hass.localize("ui.panel.lovelace.cards.energy.energy_sources_table.grid_total")}
                    </th>
                    <td
                      class="mdc-data-table__cell mdc-data-table__cell--numeric"
                    >
                      ${u(f,this.hass.locale)} kWh
                    </td>
                    ${M?r`<td
                          class="mdc-data-table__cell mdc-data-table__cell--numeric"
                        >
                          ${u(y,this.hass.locale,{style:"currency",currency:this.hass.config.currency})}
                        </td>`:""}
                  </tr>`:""}
              ${null===(h=F.gas)||void 0===h?void 0:h.map(((e,t)=>{const a=this.hass.states[e.stat_energy_from],c=g(this._data.stats[e.stat_energy_from])||0;$+=c;const b=e.stat_cost||this._data.info.cost_sensors[e.stat_energy_from],_=b?g(this._data.stats[b])||0:null;null!==_&&(z+=_);const h=t>0?this.hass.themes.darkMode?o(d(l(A)),t):i(d(l(A)),t):void 0,f=h?n(s(h)):A;return r`<tr class="mdc-data-table__row">
                  <td class="mdc-data-table__cell cell-bullet">
                    <div
                      class="bullet"
                      style=${m({borderColor:f,backgroundColor:f+"7F"})}
                    ></div>
                  </td>
                  <th class="mdc-data-table__cell" scope="row">
                    ${a?p(a):e.stat_energy_from}
                  </th>
                  <td
                    class="mdc-data-table__cell mdc-data-table__cell--numeric"
                  >
                    ${u(c,this.hass.locale)} ${S}
                  </td>
                  ${M?r`<td
                        class="mdc-data-table__cell mdc-data-table__cell--numeric"
                      >
                        ${null!==_?u(_,this.hass.locale,{style:"currency",currency:this.hass.config.currency}):""}
                      </td>`:""}
                </tr>`}))}
              ${F.gas?r`<tr class="mdc-data-table__row total">
                    <td class="mdc-data-table__cell"></td>
                    <th class="mdc-data-table__cell" scope="row">
                      ${this.hass.localize("ui.panel.lovelace.cards.energy.energy_sources_table.gas_total")}
                    </th>
                    <td
                      class="mdc-data-table__cell mdc-data-table__cell--numeric"
                    >
                      ${u($,this.hass.locale)} ${S}
                    </td>
                    ${M?r`<td
                          class="mdc-data-table__cell mdc-data-table__cell--numeric"
                        >
                          ${u(z,this.hass.locale,{style:"currency",currency:this.hass.config.currency})}
                        </td>`:""}
                  </tr>`:""}
              ${z&&y?r`<tr class="mdc-data-table__row total">
                    <td class="mdc-data-table__cell"></td>
                    <th class="mdc-data-table__cell" scope="row">
                      ${this.hass.localize("ui.panel.lovelace.cards.energy.energy_sources_table.total_costs")}
                    </th>
                    <td class="mdc-data-table__cell"></td>
                    <td
                      class="mdc-data-table__cell mdc-data-table__cell--numeric"
                    >
                      ${u(z+y,this.hass.locale,{style:"currency",currency:this.hass.config.currency})}
                    </td>
                  </tr>`:""}
            </tbody>
          </table>
        </div>
      </div>
    </ha-card>`}},{kind:"get",static:!0,key:"styles",value:function(){return b`
      ${_('export default "/**\\n * @license\\n * Copyright Google LLC All Rights Reserved.\\n *\\n * Use of this source code is governed by an MIT-style license that can be\\n * found in the LICENSE file at https://github.com/material-components/material-components-web/blob/master/LICENSE\\n */\\n.mdc-data-table__content{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;-webkit-text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit)}.mdc-data-table{background-color:#fff;background-color:var(--mdc-theme-surface, #fff);border-radius:4px;border-radius:var(--mdc-shape-medium, 4px);border-width:1px;border-style:solid;border-color:rgba(0,0,0,.12);-webkit-overflow-scrolling:touch;display:inline-flex;flex-direction:column;box-sizing:border-box;position:relative}.mdc-data-table .mdc-data-table__header-cell:first-child{border-top-left-radius:4px;border-top-left-radius:var(--mdc-shape-medium, 4px)}[dir=rtl] .mdc-data-table .mdc-data-table__header-cell:first-child,.mdc-data-table .mdc-data-table__header-cell:first-child[dir=rtl]{border-top-right-radius:4px;border-top-right-radius:var(--mdc-shape-medium, 4px);border-top-left-radius:0}.mdc-data-table .mdc-data-table__header-cell:last-child{border-top-right-radius:4px;border-top-right-radius:var(--mdc-shape-medium, 4px)}[dir=rtl] .mdc-data-table .mdc-data-table__header-cell:last-child,.mdc-data-table .mdc-data-table__header-cell:last-child[dir=rtl]{border-top-left-radius:4px;border-top-left-radius:var(--mdc-shape-medium, 4px);border-top-right-radius:0}.mdc-data-table__row{background-color:inherit}.mdc-data-table__header-cell{background-color:#fff;background-color:var(--mdc-theme-surface, #fff)}.mdc-data-table__row--selected{background-color:rgba(98, 0, 238, 0.04)}.mdc-data-table__pagination-rows-per-page-select:not(.mdc-select--disabled) .mdc-notched-outline__leading,.mdc-data-table__pagination-rows-per-page-select:not(.mdc-select--disabled) .mdc-notched-outline__notch,.mdc-data-table__pagination-rows-per-page-select:not(.mdc-select--disabled) .mdc-notched-outline__trailing{border-color:rgba(0, 0, 0, 0.12)}.mdc-data-table__cell,.mdc-data-table__header-cell{border-bottom-color:rgba(0,0,0,.12)}.mdc-data-table__pagination{border-top-color:rgba(0,0,0,.12)}.mdc-data-table__cell,.mdc-data-table__header-cell{border-bottom-width:1px;border-bottom-style:solid}.mdc-data-table__pagination{border-top-width:1px;border-top-style:solid}.mdc-data-table__row:last-child .mdc-data-table__cell{border-bottom:none}.mdc-data-table__row:not(.mdc-data-table__row--selected):hover{background-color:rgba(0, 0, 0, 0.04)}.mdc-data-table__header-cell{color:rgba(0, 0, 0, 0.87)}.mdc-data-table__pagination-total,.mdc-data-table__pagination-rows-per-page-label,.mdc-data-table__cell{color:rgba(0, 0, 0, 0.87)}.mdc-data-table__row{height:52px}.mdc-data-table__pagination{min-height:52px}.mdc-data-table__header-row{height:56px}.mdc-data-table__cell,.mdc-data-table__header-cell{padding:0 16px 0 16px}.mdc-data-table__header-cell--checkbox,.mdc-data-table__cell--checkbox{padding-left:4px;padding-right:0}[dir=rtl] .mdc-data-table__header-cell--checkbox,[dir=rtl] .mdc-data-table__cell--checkbox,.mdc-data-table__header-cell--checkbox[dir=rtl],.mdc-data-table__cell--checkbox[dir=rtl]{padding-left:0;padding-right:4px}.mdc-data-table__sort-icon-button{color:rgba(0, 0, 0, 0.6)}.mdc-data-table__sort-icon-button .mdc-icon-button__ripple::before,.mdc-data-table__sort-icon-button .mdc-icon-button__ripple::after{background-color:rgba(0, 0, 0, 0.6);background-color:var(--mdc-ripple-color, rgba(0, 0, 0, 0.6))}.mdc-data-table__sort-icon-button:hover .mdc-icon-button__ripple::before,.mdc-data-table__sort-icon-button.mdc-ripple-surface--hover .mdc-icon-button__ripple::before{opacity:0.04;opacity:var(--mdc-ripple-hover-opacity, 0.04)}.mdc-data-table__sort-icon-button.mdc-ripple-upgraded--background-focused .mdc-icon-button__ripple::before,.mdc-data-table__sort-icon-button:not(.mdc-ripple-upgraded):focus .mdc-icon-button__ripple::before{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-focus-opacity, 0.12)}.mdc-data-table__sort-icon-button:not(.mdc-ripple-upgraded) .mdc-icon-button__ripple::after{transition:opacity 150ms linear}.mdc-data-table__sort-icon-button:not(.mdc-ripple-upgraded):active .mdc-icon-button__ripple::after{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-data-table__sort-icon-button.mdc-ripple-upgraded{--mdc-ripple-fg-opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-data-table__header-cell--sorted .mdc-data-table__sort-icon-button{color:rgba(0, 0, 0, 0.87)}.mdc-data-table__header-cell--sorted .mdc-data-table__sort-icon-button .mdc-icon-button__ripple::before,.mdc-data-table__header-cell--sorted .mdc-data-table__sort-icon-button .mdc-icon-button__ripple::after{background-color:rgba(0, 0, 0, 0.87);background-color:var(--mdc-ripple-color, rgba(0, 0, 0, 0.87))}.mdc-data-table__header-cell--sorted .mdc-data-table__sort-icon-button:hover .mdc-icon-button__ripple::before,.mdc-data-table__header-cell--sorted .mdc-data-table__sort-icon-button.mdc-ripple-surface--hover .mdc-icon-button__ripple::before{opacity:0.04;opacity:var(--mdc-ripple-hover-opacity, 0.04)}.mdc-data-table__header-cell--sorted .mdc-data-table__sort-icon-button.mdc-ripple-upgraded--background-focused .mdc-icon-button__ripple::before,.mdc-data-table__header-cell--sorted .mdc-data-table__sort-icon-button:not(.mdc-ripple-upgraded):focus .mdc-icon-button__ripple::before{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-focus-opacity, 0.12)}.mdc-data-table__header-cell--sorted .mdc-data-table__sort-icon-button:not(.mdc-ripple-upgraded) .mdc-icon-button__ripple::after{transition:opacity 150ms linear}.mdc-data-table__header-cell--sorted .mdc-data-table__sort-icon-button:not(.mdc-ripple-upgraded):active .mdc-icon-button__ripple::after{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-data-table__header-cell--sorted .mdc-data-table__sort-icon-button.mdc-ripple-upgraded{--mdc-ripple-fg-opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-data-table__table-container{-webkit-overflow-scrolling:touch;overflow-x:auto;width:100%}.mdc-data-table__table{min-width:100%;border:0;white-space:nowrap;border-spacing:0;table-layout:fixed}.mdc-data-table__cell{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;-webkit-text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);box-sizing:border-box;overflow:hidden;text-align:left;text-overflow:ellipsis}[dir=rtl] .mdc-data-table__cell,.mdc-data-table__cell[dir=rtl]{text-align:right}.mdc-data-table__cell--numeric{text-align:right}[dir=rtl] .mdc-data-table__cell--numeric,.mdc-data-table__cell--numeric[dir=rtl]{text-align:left}.mdc-data-table__cell--checkbox{width:1px}.mdc-data-table__header-cell{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-subtitle2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-subtitle2-font-size, 0.875rem);line-height:1.375rem;line-height:var(--mdc-typography-subtitle2-line-height, 1.375rem);font-weight:500;font-weight:var(--mdc-typography-subtitle2-font-weight, 500);letter-spacing:0.0071428571em;letter-spacing:var(--mdc-typography-subtitle2-letter-spacing, 0.0071428571em);text-decoration:inherit;-webkit-text-decoration:var(--mdc-typography-subtitle2-text-decoration, inherit);text-decoration:var(--mdc-typography-subtitle2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-subtitle2-text-transform, inherit);box-sizing:border-box;text-overflow:ellipsis;overflow:hidden;outline:none;text-align:left}[dir=rtl] .mdc-data-table__header-cell,.mdc-data-table__header-cell[dir=rtl]{text-align:right}.mdc-data-table__header-cell--checkbox{width:1px}.mdc-data-table__header-cell--numeric{text-align:right}[dir=rtl] .mdc-data-table__header-cell--numeric,.mdc-data-table__header-cell--numeric[dir=rtl]{text-align:left}.mdc-data-table__sort-icon-button{width:28px;height:28px;padding:2px;-webkit-transform:rotate(0.0001deg);transform:rotate(0.0001deg);margin-left:4px;margin-right:0;transition:-webkit-transform 150ms 0ms cubic-bezier(0.4, 0, 0.2, 1);transition:transform 150ms 0ms cubic-bezier(0.4, 0, 0.2, 1);transition:transform 150ms 0ms cubic-bezier(0.4, 0, 0.2, 1), -webkit-transform 150ms 0ms cubic-bezier(0.4, 0, 0.2, 1);opacity:0}.mdc-data-table__sort-icon-button.mdc-icon-button--reduced-size .mdc-icon-button__ripple{width:28px;height:28px;margin-top:0px;margin-bottom:0px;margin-right:0px;margin-left:0px}.mdc-data-table__sort-icon-button .mdc-icon-button__touch{position:absolute;top:50%;height:28px;left:50%;width:28px;-webkit-transform:translate(-50%, -50%);transform:translate(-50%, -50%)}[dir=rtl] .mdc-data-table__sort-icon-button,.mdc-data-table__sort-icon-button[dir=rtl]{margin-left:0;margin-right:4px}.mdc-data-table__header-cell--numeric .mdc-data-table__sort-icon-button{margin-left:0;margin-right:4px}[dir=rtl] .mdc-data-table__header-cell--numeric .mdc-data-table__sort-icon-button,.mdc-data-table__header-cell--numeric .mdc-data-table__sort-icon-button[dir=rtl]{margin-left:4px;margin-right:0}.mdc-data-table__header-cell--sorted-descending .mdc-data-table__sort-icon-button{-webkit-transform:rotate(-180deg);transform:rotate(-180deg)}.mdc-data-table__sort-icon-button:focus,.mdc-data-table__header-cell:hover .mdc-data-table__sort-icon-button,.mdc-data-table__header-cell--sorted .mdc-data-table__sort-icon-button{opacity:1}.mdc-data-table__header-cell-wrapper{align-items:center;display:inline-flex;vertical-align:middle}.mdc-data-table__header-cell--with-sort{cursor:pointer}.mdc-data-table__sort-status-label{clip:rect(1px, 1px, 1px, 1px);height:1px;overflow:hidden;position:absolute;white-space:nowrap;width:1px}.mdc-data-table__progress-indicator{display:none;position:absolute;width:100%}.mdc-data-table--in-progress .mdc-data-table__progress-indicator{display:block}.mdc-data-table__scrim{background-color:#fff;background-color:var(--mdc-theme-surface, #fff);height:100%;opacity:.32;position:absolute;top:0;width:100%}.mdc-data-table--sticky-header .mdc-data-table__header-cell{position:-webkit-sticky;position:sticky;top:0;z-index:1}.mdc-data-table__pagination{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;-webkit-text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);box-sizing:border-box;display:flex;justify-content:flex-end}.mdc-data-table__pagination-trailing{margin-left:4px;margin-right:0;align-items:center;display:flex;flex-wrap:wrap;justify-content:flex-end}[dir=rtl] .mdc-data-table__pagination-trailing,.mdc-data-table__pagination-trailing[dir=rtl]{margin-left:0;margin-right:4px}.mdc-data-table__pagination-navigation{align-items:center;display:flex}.mdc-data-table__pagination-button{margin-left:0;margin-right:4px}[dir=rtl] .mdc-data-table__pagination-button .mdc-button__icon,.mdc-data-table__pagination-button .mdc-button__icon[dir=rtl]{-webkit-transform:rotate(180deg);transform:rotate(180deg)}[dir=rtl] .mdc-data-table__pagination-button,.mdc-data-table__pagination-button[dir=rtl]{margin-left:4px;margin-right:0}.mdc-data-table__pagination-total{margin-left:14px;margin-right:36px;white-space:nowrap}[dir=rtl] .mdc-data-table__pagination-total,.mdc-data-table__pagination-total[dir=rtl]{margin-left:36px;margin-right:14px}.mdc-data-table__pagination-rows-per-page{margin-left:0;margin-right:22px;align-items:center;display:inline-flex}[dir=rtl] .mdc-data-table__pagination-rows-per-page,.mdc-data-table__pagination-rows-per-page[dir=rtl]{margin-left:22px;margin-right:0}.mdc-data-table__pagination-rows-per-page-label{margin-left:0;margin-right:12px;white-space:nowrap}[dir=rtl] .mdc-data-table__pagination-rows-per-page-label,.mdc-data-table__pagination-rows-per-page-label[dir=rtl]{margin-left:12px;margin-right:0}.mdc-data-table__pagination-rows-per-page-select{min-width:80px;min-width:var(--mdc-menu-min-width, 80px);margin:8px 0}.mdc-data-table__pagination-rows-per-page-select .mdc-select__anchor{width:100%;min-width:80px}.mdc-data-table__pagination-rows-per-page-select .mdc-select__anchor{height:36px}.mdc-data-table__pagination-rows-per-page-select .mdc-select__anchor .mdc-floating-label--float-above{-webkit-transform:translateY(-27.25px) scale(1);transform:translateY(-27.25px) scale(1)}.mdc-data-table__pagination-rows-per-page-select .mdc-select__anchor .mdc-floating-label--float-above{font-size:.75rem}.mdc-data-table__pagination-rows-per-page-select .mdc-select__anchor.mdc-notched-outline--upgraded .mdc-floating-label--float-above,.mdc-data-table__pagination-rows-per-page-select .mdc-select__anchor .mdc-notched-outline--upgraded .mdc-floating-label--float-above{-webkit-transform:translateY(-24.75px) scale(0.75);transform:translateY(-24.75px) scale(0.75)}.mdc-data-table__pagination-rows-per-page-select .mdc-select__anchor.mdc-notched-outline--upgraded .mdc-floating-label--float-above,.mdc-data-table__pagination-rows-per-page-select .mdc-select__anchor .mdc-notched-outline--upgraded .mdc-floating-label--float-above{font-size:1rem}.mdc-data-table__pagination-rows-per-page-select .mdc-select__anchor .mdc-floating-label--shake{-webkit-animation:mdc-floating-label-shake-float-above-select-outlined-36px 250ms 1;animation:mdc-floating-label-shake-float-above-select-outlined-36px 250ms 1}@-webkit-keyframes mdc-floating-label-shake-float-above-select-outlined-36px{0%{-webkit-transform:translateX(calc(0 - 0%)) translateY(-24.75px) scale(0.75);transform:translateX(calc(0 - 0%)) translateY(-24.75px) scale(0.75)}33%{-webkit-animation-timing-function:cubic-bezier(0.5, 0, 0.701732, 0.495819);animation-timing-function:cubic-bezier(0.5, 0, 0.701732, 0.495819);-webkit-transform:translateX(calc(4% - 0%)) translateY(-24.75px) scale(0.75);transform:translateX(calc(4% - 0%)) translateY(-24.75px) scale(0.75)}66%{-webkit-animation-timing-function:cubic-bezier(0.302435, 0.381352, 0.55, 0.956352);animation-timing-function:cubic-bezier(0.302435, 0.381352, 0.55, 0.956352);-webkit-transform:translateX(calc(-4% - 0%)) translateY(-24.75px) scale(0.75);transform:translateX(calc(-4% - 0%)) translateY(-24.75px) scale(0.75)}100%{-webkit-transform:translateX(calc(0 - 0%)) translateY(-24.75px) scale(0.75);transform:translateX(calc(0 - 0%)) translateY(-24.75px) scale(0.75)}}@keyframes mdc-floating-label-shake-float-above-select-outlined-36px{0%{-webkit-transform:translateX(calc(0 - 0%)) translateY(-24.75px) scale(0.75);transform:translateX(calc(0 - 0%)) translateY(-24.75px) scale(0.75)}33%{-webkit-animation-timing-function:cubic-bezier(0.5, 0, 0.701732, 0.495819);animation-timing-function:cubic-bezier(0.5, 0, 0.701732, 0.495819);-webkit-transform:translateX(calc(4% - 0%)) translateY(-24.75px) scale(0.75);transform:translateX(calc(4% - 0%)) translateY(-24.75px) scale(0.75)}66%{-webkit-animation-timing-function:cubic-bezier(0.302435, 0.381352, 0.55, 0.956352);animation-timing-function:cubic-bezier(0.302435, 0.381352, 0.55, 0.956352);-webkit-transform:translateX(calc(-4% - 0%)) translateY(-24.75px) scale(0.75);transform:translateX(calc(-4% - 0%)) translateY(-24.75px) scale(0.75)}100%{-webkit-transform:translateX(calc(0 - 0%)) translateY(-24.75px) scale(0.75);transform:translateX(calc(0 - 0%)) translateY(-24.75px) scale(0.75)}}.mdc-data-table__pagination-rows-per-page-select .mdc-select__dropdown-icon{width:20px;height:20px}.mdc-data-table__pagination-rows-per-page-select.mdc-select--outlined .mdc-select__anchor :not(.mdc-notched-outline--notched) .mdc-notched-outline__notch{max-width:calc(100% - 56px)}.mdc-data-table__pagination-rows-per-page-select .mdc-list-item.mdc-list-item--with-one-line{height:36px}.mdc-data-table__header-row-checkbox.mdc-checkbox--selected .mdc-checkbox__ripple::before,.mdc-data-table__header-row-checkbox.mdc-checkbox--selected .mdc-checkbox__ripple::after,.mdc-data-table__row-checkbox.mdc-checkbox--selected .mdc-checkbox__ripple::before,.mdc-data-table__row-checkbox.mdc-checkbox--selected .mdc-checkbox__ripple::after{background-color:#6200ee;background-color:var(--mdc-ripple-color, var(--mdc-theme-primary, #6200ee))}.mdc-data-table__header-row-checkbox.mdc-checkbox--selected:hover .mdc-checkbox__ripple::before,.mdc-data-table__header-row-checkbox.mdc-checkbox--selected.mdc-ripple-surface--hover .mdc-checkbox__ripple::before,.mdc-data-table__row-checkbox.mdc-checkbox--selected:hover .mdc-checkbox__ripple::before,.mdc-data-table__row-checkbox.mdc-checkbox--selected.mdc-ripple-surface--hover .mdc-checkbox__ripple::before{opacity:0.04;opacity:var(--mdc-ripple-hover-opacity, 0.04)}.mdc-data-table__header-row-checkbox.mdc-checkbox--selected.mdc-ripple-upgraded--background-focused .mdc-checkbox__ripple::before,.mdc-data-table__header-row-checkbox.mdc-checkbox--selected:not(.mdc-ripple-upgraded):focus .mdc-checkbox__ripple::before,.mdc-data-table__row-checkbox.mdc-checkbox--selected.mdc-ripple-upgraded--background-focused .mdc-checkbox__ripple::before,.mdc-data-table__row-checkbox.mdc-checkbox--selected:not(.mdc-ripple-upgraded):focus .mdc-checkbox__ripple::before{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-focus-opacity, 0.12)}.mdc-data-table__header-row-checkbox.mdc-checkbox--selected:not(.mdc-ripple-upgraded) .mdc-checkbox__ripple::after,.mdc-data-table__row-checkbox.mdc-checkbox--selected:not(.mdc-ripple-upgraded) .mdc-checkbox__ripple::after{transition:opacity 150ms linear}.mdc-data-table__header-row-checkbox.mdc-checkbox--selected:not(.mdc-ripple-upgraded):active .mdc-checkbox__ripple::after,.mdc-data-table__row-checkbox.mdc-checkbox--selected:not(.mdc-ripple-upgraded):active .mdc-checkbox__ripple::after{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-data-table__header-row-checkbox.mdc-checkbox--selected.mdc-ripple-upgraded,.mdc-data-table__row-checkbox.mdc-checkbox--selected.mdc-ripple-upgraded{--mdc-ripple-fg-opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-data-table__header-row-checkbox.mdc-ripple-upgraded--background-focused.mdc-checkbox--selected .mdc-checkbox__ripple::before,.mdc-data-table__header-row-checkbox.mdc-ripple-upgraded--background-focused.mdc-checkbox--selected .mdc-checkbox__ripple::after,.mdc-data-table__row-checkbox.mdc-ripple-upgraded--background-focused.mdc-checkbox--selected .mdc-checkbox__ripple::before,.mdc-data-table__row-checkbox.mdc-ripple-upgraded--background-focused.mdc-checkbox--selected .mdc-checkbox__ripple::after{background-color:#6200ee;background-color:var(--mdc-ripple-color, var(--mdc-theme-primary, #6200ee))}.mdc-data-table__header-row-checkbox .mdc-checkbox__native-control:enabled:not(:checked):not(:indeterminate):not([data-indeterminate=true])~.mdc-checkbox__background,.mdc-data-table__row-checkbox .mdc-checkbox__native-control:enabled:not(:checked):not(:indeterminate):not([data-indeterminate=true])~.mdc-checkbox__background{border-color:rgba(0, 0, 0, 0.54);border-color:var(--mdc-checkbox-unchecked-color, rgba(0, 0, 0, 0.54));background-color:transparent}.mdc-data-table__header-row-checkbox .mdc-checkbox__native-control:enabled:checked~.mdc-checkbox__background,.mdc-data-table__header-row-checkbox .mdc-checkbox__native-control:enabled:indeterminate~.mdc-checkbox__background,.mdc-data-table__header-row-checkbox .mdc-checkbox__native-control[data-indeterminate=true]:enabled~.mdc-checkbox__background,.mdc-data-table__row-checkbox .mdc-checkbox__native-control:enabled:checked~.mdc-checkbox__background,.mdc-data-table__row-checkbox .mdc-checkbox__native-control:enabled:indeterminate~.mdc-checkbox__background,.mdc-data-table__row-checkbox .mdc-checkbox__native-control[data-indeterminate=true]:enabled~.mdc-checkbox__background{border-color:#6200ee;border-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #6200ee));background-color:#6200ee;background-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #6200ee))}@-webkit-keyframes mdc-checkbox-fade-in-background-8A000000FF6200EE00000000FF6200EE{0%{border-color:rgba(0, 0, 0, 0.54);border-color:var(--mdc-checkbox-unchecked-color, rgba(0, 0, 0, 0.54));background-color:transparent}50%{border-color:#6200ee;border-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #6200ee));background-color:#6200ee;background-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #6200ee))}}@keyframes mdc-checkbox-fade-in-background-8A000000FF6200EE00000000FF6200EE{0%{border-color:rgba(0, 0, 0, 0.54);border-color:var(--mdc-checkbox-unchecked-color, rgba(0, 0, 0, 0.54));background-color:transparent}50%{border-color:#6200ee;border-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #6200ee));background-color:#6200ee;background-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #6200ee))}}@-webkit-keyframes mdc-checkbox-fade-out-background-8A000000FF6200EE00000000FF6200EE{0%,80%{border-color:#6200ee;border-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #6200ee));background-color:#6200ee;background-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #6200ee))}100%{border-color:rgba(0, 0, 0, 0.54);border-color:var(--mdc-checkbox-unchecked-color, rgba(0, 0, 0, 0.54));background-color:transparent}}@keyframes mdc-checkbox-fade-out-background-8A000000FF6200EE00000000FF6200EE{0%,80%{border-color:#6200ee;border-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #6200ee));background-color:#6200ee;background-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #6200ee))}100%{border-color:rgba(0, 0, 0, 0.54);border-color:var(--mdc-checkbox-unchecked-color, rgba(0, 0, 0, 0.54));background-color:transparent}}.mdc-data-table__header-row-checkbox.mdc-checkbox--anim-unchecked-checked .mdc-checkbox__native-control:enabled~.mdc-checkbox__background,.mdc-data-table__header-row-checkbox.mdc-checkbox--anim-unchecked-indeterminate .mdc-checkbox__native-control:enabled~.mdc-checkbox__background,.mdc-data-table__row-checkbox.mdc-checkbox--anim-unchecked-checked .mdc-checkbox__native-control:enabled~.mdc-checkbox__background,.mdc-data-table__row-checkbox.mdc-checkbox--anim-unchecked-indeterminate .mdc-checkbox__native-control:enabled~.mdc-checkbox__background{-webkit-animation-name:mdc-checkbox-fade-in-background-8A000000FF6200EE00000000FF6200EE;animation-name:mdc-checkbox-fade-in-background-8A000000FF6200EE00000000FF6200EE}.mdc-data-table__header-row-checkbox.mdc-checkbox--anim-checked-unchecked .mdc-checkbox__native-control:enabled~.mdc-checkbox__background,.mdc-data-table__header-row-checkbox.mdc-checkbox--anim-indeterminate-unchecked .mdc-checkbox__native-control:enabled~.mdc-checkbox__background,.mdc-data-table__row-checkbox.mdc-checkbox--anim-checked-unchecked .mdc-checkbox__native-control:enabled~.mdc-checkbox__background,.mdc-data-table__row-checkbox.mdc-checkbox--anim-indeterminate-unchecked .mdc-checkbox__native-control:enabled~.mdc-checkbox__background{-webkit-animation-name:mdc-checkbox-fade-out-background-8A000000FF6200EE00000000FF6200EE;animation-name:mdc-checkbox-fade-out-background-8A000000FF6200EE00000000FF6200EE}\\n\\n/*# sourceMappingURL=mdc.data-table.min.css.map*/";')}
      .mdc-data-table {
        width: 100%;
        border: 0;
      }
      .mdc-data-table__header-cell,
      .mdc-data-table__cell {
        color: var(--primary-text-color);
        border-bottom-color: var(--divider-color);
      }
      .mdc-data-table__row:not(.mdc-data-table__row--selected):hover {
        background-color: rgba(var(--rgb-primary-text-color), 0.04);
      }
      .total {
        --mdc-typography-body2-font-weight: 500;
      }
      .total .mdc-data-table__cell {
        border-top: 1px solid var(--divider-color);
      }
      ha-card {
        height: 100%;
      }
      .card-header {
        padding-bottom: 0;
      }
      .content {
        padding: 16px;
      }
      .has-header {
        padding-top: 0;
      }
      .cell-bullet {
        width: 32px;
        padding-right: 0;
      }
      .bullet {
        border-width: 1px;
        border-style: solid;
        border-radius: 4px;
        height: 16px;
        width: 32px;
      }
    `}}]}}),y(t));export{v as HuiEnergySourcesTableCard};
