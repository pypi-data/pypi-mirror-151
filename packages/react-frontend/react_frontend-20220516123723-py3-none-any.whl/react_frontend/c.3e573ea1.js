import{_ as e,s as t,e as a,t as i,$ as l,ct as o,f as r,ar as d,n as s,cu as n,ap as c,g as h,i as u,aq as b,aA as m,ax as p,bw as v,bu as f,m as _,au as k,cv as g,at as y,av as w}from"./main-ac83c92b.js";import{s as x,c as $,r as R,d as C,n as D,b as z,i as T,e as P}from"./c.027db416.js";import{c as B}from"./c.39da0aeb.js";import{f as F}from"./c.5b2e0d05.js";import"./c.be47aa9a.js";import"./c.53212acc.js";import"./c.4860f91b.js";import"./c.e9aa747b.js";import"./c.0660f3f3.js";import"./c.c8193d47.js";import{w as S}from"./c.d2605417.js";function H(e){if(!e||"object"!=typeof e)return e;if("[object Date]"==Object.prototype.toString.call(e))return new Date(e.getTime());if(Array.isArray(e))return e.map(H);var t={};return Object.keys(e).forEach((function(a){t[a]=H(e[a])})),t}let j;e([s("ha-button-related-filter-menu")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[a()],key:"hass",value:void 0},{kind:"field",decorators:[a()],key:"corner",value:()=>"TOP_START"},{kind:"field",decorators:[a({type:Boolean,reflect:!0})],key:"narrow",value:()=>!1},{kind:"field",decorators:[a({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[a({attribute:!1})],key:"value",value:void 0},{kind:"field",decorators:[a({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[i()],key:"_open",value:()=>!1},{kind:"method",key:"render",value:function(){var e,t,a;return l`
      <ha-icon-button
        @click=${this._handleClick}
        .label=${this.hass.localize("ui.components.related-filter-menu.filter")}
        .path=${o}
      ></ha-icon-button>
      <mwc-menu-surface
        .open=${this._open}
        .anchor=${this}
        .fullwidth=${this.narrow}
        .corner=${this.corner}
        @closed=${this._onClosed}
        @input=${x}
      >
        <ha-area-picker
          .label=${this.hass.localize("ui.components.related-filter-menu.filter_by_area")}
          .hass=${this.hass}
          .value=${null===(e=this.value)||void 0===e?void 0:e.area}
          no-add
          @value-changed=${this._areaPicked}
          @click=${this._preventDefault}
        ></ha-area-picker>
        <ha-device-picker
          .label=${this.hass.localize("ui.components.related-filter-menu.filter_by_device")}
          .hass=${this.hass}
          .value=${null===(t=this.value)||void 0===t?void 0:t.device}
          @value-changed=${this._devicePicked}
          @click=${this._preventDefault}
        ></ha-device-picker>
        <ha-entity-picker
          .label=${this.hass.localize("ui.components.related-filter-menu.filter_by_entity")}
          .hass=${this.hass}
          .value=${null===(a=this.value)||void 0===a?void 0:a.entity}
          .excludeDomains=${this.excludeDomains}
          @value-changed=${this._entityPicked}
          @click=${this._preventDefault}
        ></ha-entity-picker>
      </mwc-menu-surface>
    `}},{kind:"method",key:"_handleClick",value:function(){this.disabled||(this._open=!0)}},{kind:"method",key:"_onClosed",value:function(e){e.stopPropagation(),this._open=!1}},{kind:"method",key:"_preventDefault",value:function(e){e.preventDefault()}},{kind:"method",key:"_entityPicked",value:async function(e){e.stopPropagation();const t=e.detail.value;if(!t)return void r(this,"related-changed",{value:void 0});const a=this.hass.localize("ui.components.related-filter-menu.filtered_by_entity","entity_name",$(e.currentTarget.comboBox.selectedItem)),i=await F(this.hass,"entity",t);r(this,"related-changed",{value:{entity:t},filter:a,items:i})}},{kind:"method",key:"_devicePicked",value:async function(e){e.stopPropagation();const t=e.detail.value;if(!t)return void r(this,"related-changed",{value:void 0});const a=this.hass.localize("ui.components.related-filter-menu.filtered_by_device","device_name",B(e.currentTarget.comboBox.selectedItem,this.hass)),i=await F(this.hass,"device",t);r(this,"related-changed",{value:{device:t},filter:a,items:i})}},{kind:"method",key:"_areaPicked",value:async function(e){e.stopPropagation();const t=e.detail.value;if(!t)return void r(this,"related-changed",{value:void 0});const a=this.hass.localize("ui.components.related-filter-menu.filtered_by_area","area_name",e.currentTarget.comboBox.selectedItem.name),i=await F(this.hass,"area",t);r(this,"related-changed",{value:{area:t},filter:a,items:i})}},{kind:"get",static:!0,key:"styles",value:function(){return d`
      :host {
        display: inline-block;
        position: relative;
        --mdc-menu-min-width: 250px;
      }
      ha-area-picker,
      ha-device-picker,
      ha-entity-picker {
        display: block;
        width: 300px;
        padding: 4px 16px;
        box-sizing: border-box;
      }
      ha-area-picker {
        padding-top: 16px;
      }
      ha-entity-picker {
        padding-bottom: 16px;
      }
      :host([narrow]) ha-area-picker,
      :host([narrow]) ha-device-picker,
      :host([narrow]) ha-entity-picker {
        width: 100%;
      }
    `}}]}}),t),e([s("ha-icon-overflow-menu")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a({type:Array})],key:"items",value:()=>[]},{kind:"field",decorators:[a({type:Boolean})],key:"narrow",value:()=>!1},{kind:"method",key:"render",value:function(){return l`
      ${this.narrow?l` <!-- Collapsed representation for small screens -->
            <ha-button-menu
              @click=${this._handleIconOverflowMenuOpened}
              @closed=${this._handleIconOverflowMenuClosed}
              class="ha-icon-overflow-menu-overflow"
              corner="BOTTOM_START"
              absolute
            >
              <ha-icon-button
                .label=${this.hass.localize("ui.common.overflow_menu")}
                .path=${n}
                slot="trigger"
              ></ha-icon-button>

              ${this.items.map((e=>l`
                  <mwc-list-item
                    graphic="icon"
                    .disabled=${e.disabled}
                    @click=${e.action}
                  >
                    <div slot="graphic">
                      <ha-svg-icon .path=${e.path}></ha-svg-icon>
                    </div>
                    ${e.label}
                  </mwc-list-item>
                `))}
            </ha-button-menu>`:l`
            <!-- Icon representation for big screens -->
            ${this.items.map((e=>e.narrowOnly?"":l`<div>
                    ${e.tooltip?l`<paper-tooltip animation-delay="0" position="left">
                          ${e.tooltip}
                        </paper-tooltip>`:""}
                    <ha-icon-button
                      @click=${e.action}
                      .label=${e.label}
                      .path=${e.path}
                      .disabled=${e.disabled}
                    ></ha-icon-button>
                  </div> `))}
          `}
    `}},{kind:"method",key:"_handleIconOverflowMenuOpened",value:function(){const e=this.closest(".mdc-data-table__row");e&&(e.style.zIndex="1")}},{kind:"method",key:"_handleIconOverflowMenuClosed",value:function(){const e=this.closest(".mdc-data-table__row");e&&(e.style.zIndex="")}},{kind:"get",static:!0,key:"styles",value:function(){return d`
      :host {
        display: flex;
        justify-content: flex-end;
      }
    `}}]}}),t);e([s("ha-data-table")],(function(e,t){class o extends t{constructor(...t){super(...t),e(this)}}return{F:o,d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a({type:Object})],key:"columns",value:()=>({})},{kind:"field",decorators:[a({type:Array})],key:"data",value:()=>[]},{kind:"field",decorators:[a({type:Boolean})],key:"selectable",value:()=>!1},{kind:"field",decorators:[a({type:Boolean})],key:"clickable",value:()=>!1},{kind:"field",decorators:[a({type:Boolean})],key:"hasFab",value:()=>!1},{kind:"field",decorators:[a({attribute:!1})],key:"appendRow",value:void 0},{kind:"field",decorators:[a({type:Boolean,attribute:"auto-height"})],key:"autoHeight",value:()=>!1},{kind:"field",decorators:[a({type:String})],key:"id",value:()=>"id"},{kind:"field",decorators:[a({type:String})],key:"noDataText",value:void 0},{kind:"field",decorators:[a({type:String})],key:"searchLabel",value:void 0},{kind:"field",decorators:[a({type:Boolean,attribute:"no-label-float"})],key:"noLabelFloat",value:()=>!1},{kind:"field",decorators:[a({type:String})],key:"filter",value:()=>""},{kind:"field",decorators:[i()],key:"_filterable",value:()=>!1},{kind:"field",decorators:[i()],key:"_filter",value:()=>""},{kind:"field",decorators:[i()],key:"_sortColumn",value:void 0},{kind:"field",decorators:[i()],key:"_sortDirection",value:()=>null},{kind:"field",decorators:[i()],key:"_filteredData",value:()=>[]},{kind:"field",decorators:[i()],key:"_headerHeight",value:()=>0},{kind:"field",decorators:[c("slot[name='header']")],key:"_header",value:void 0},{kind:"field",decorators:[i()],key:"_items",value:()=>[]},{kind:"field",key:"_checkableRowsCount",value:void 0},{kind:"field",key:"_checkedRows",value:()=>[]},{kind:"field",key:"_sortColumns",value:()=>({})},{kind:"field",key:"curRequest",value:()=>0},{kind:"field",decorators:[R(".scroller")],key:"_savedScrollPos",value:void 0},{kind:"field",key:"_debounceSearch",value(){return C((e=>{this._filter=e}),100,!1)}},{kind:"method",key:"clearSelection",value:function(){this._checkedRows=[],this._checkedRowsChanged()}},{kind:"method",key:"connectedCallback",value:function(){h(u(o.prototype),"connectedCallback",this).call(this),this._items.length&&(this._items=[...this._items])}},{kind:"method",key:"firstUpdated",value:function(){this.updateComplete.then((()=>this._calcTableHeight()))}},{kind:"method",key:"willUpdate",value:function(e){if(h(u(o.prototype),"willUpdate",this).call(this,e),e.has("columns")){this._filterable=Object.values(this.columns).some((e=>e.filterable));for(const e in this.columns)if(this.columns[e].direction){this._sortDirection=this.columns[e].direction,this._sortColumn=e;break}const e=H(this.columns);Object.values(e).forEach((e=>{delete e.title,delete e.type,delete e.template})),this._sortColumns=e}e.has("filter")&&this._debounceSearch(this.filter),e.has("data")&&(this._checkableRowsCount=this.data.filter((e=>!1!==e.selectable)).length),(e.has("data")||e.has("columns")||e.has("_filter")||e.has("_sortColumn")||e.has("_sortDirection"))&&this._sortFilterData()}},{kind:"method",key:"render",value:function(){return l`
      <div class="mdc-data-table">
        <slot name="header" @slotchange=${this._calcTableHeight}>
          ${this._filterable?l`
                <div class="table-header">
                  <search-input
                    .hass=${this.hass}
                    @value-changed=${this._handleSearchChange}
                    .label=${this.searchLabel}
                    .noLabelFloat=${this.noLabelFloat}
                  ></search-input>
                </div>
              `:""}
        </slot>
        <div
          class="mdc-data-table__table ${b({"auto-height":this.autoHeight})}"
          role="table"
          aria-rowcount=${this._filteredData.length+1}
          style=${m({height:this.autoHeight?53*(this._filteredData.length||1)+53+"px":`calc(100% - ${this._headerHeight}px)`})}
        >
          <div class="mdc-data-table__header-row" role="row" aria-rowindex="1">
            ${this.selectable?l`
                  <div
                    class="mdc-data-table__header-cell mdc-data-table__header-cell--checkbox"
                    role="columnheader"
                  >
                    <ha-checkbox
                      class="mdc-data-table__row-checkbox"
                      @change=${this._handleHeaderRowCheckboxClick}
                      .indeterminate=${this._checkedRows.length&&this._checkedRows.length!==this._checkableRowsCount}
                      .checked=${this._checkedRows.length===this._checkableRowsCount}
                    >
                    </ha-checkbox>
                  </div>
                `:""}
            ${Object.entries(this.columns).map((([e,t])=>{if(t.hidden)return"";const a=e===this._sortColumn,i={"mdc-data-table__header-cell--numeric":"numeric"===t.type,"mdc-data-table__header-cell--icon":"icon"===t.type,"mdc-data-table__header-cell--icon-button":"icon-button"===t.type,"mdc-data-table__header-cell--overflow-menu":"overflow-menu"===t.type,sortable:Boolean(t.sortable),"not-sorted":Boolean(t.sortable&&!a),grows:Boolean(t.grows)};return l`
                <div
                  aria-label=${t.label}
                  class="mdc-data-table__header-cell ${b(i)}"
                  style=${t.width?m({[t.grows?"minWidth":"width"]:t.width,maxWidth:t.maxWidth||""}):""}
                  role="columnheader"
                  aria-sort=${p(a?"desc"===this._sortDirection?"descending":"ascending":void 0)}
                  @click=${this._handleHeaderClick}
                  .columnId=${e}
                >
                  ${t.sortable?l`
                        <ha-svg-icon
                          .path=${a&&"desc"===this._sortDirection?v:f}
                        ></ha-svg-icon>
                      `:""}
                  <span>${t.title}</span>
                </div>
              `}))}
          </div>
          ${this._filteredData.length?l`
                <lit-virtualizer
                  scroller
                  class="mdc-data-table__content scroller ha-scrollbar"
                  @scroll=${this._saveScrollPos}
                  .items=${this._items}
                  .renderItem=${this._renderRow}
                ></lit-virtualizer>
              `:l`
                <div class="mdc-data-table__content">
                  <div class="mdc-data-table__row" role="row">
                    <div class="mdc-data-table__cell grows center" role="cell">
                      ${this.noDataText||"No data"}
                    </div>
                  </div>
                </div>
              `}
        </div>
      </div>
    `}},{kind:"field",key:"_renderRow",value(){return(e,t)=>e?e.append?l` <div class="mdc-data-table__row">${e.content}</div> `:e.empty?l` <div class="mdc-data-table__row"></div> `:l`
      <div
        aria-rowindex=${t+2}
        role="row"
        .rowId=${e[this.id]}
        @click=${this._handleRowClick}
        class="mdc-data-table__row ${b({"mdc-data-table__row--selected":this._checkedRows.includes(String(e[this.id])),clickable:this.clickable})}"
        aria-selected=${p(!!this._checkedRows.includes(String(e[this.id]))||void 0)}
        .selectable=${!1!==e.selectable}
      >
        ${this.selectable?l`
              <div
                class="mdc-data-table__cell mdc-data-table__cell--checkbox"
                role="cell"
              >
                <ha-checkbox
                  class="mdc-data-table__row-checkbox"
                  @change=${this._handleRowCheckboxClick}
                  .rowId=${e[this.id]}
                  .disabled=${!1===e.selectable}
                  .checked=${this._checkedRows.includes(String(e[this.id]))}
                >
                </ha-checkbox>
              </div>
            `:""}
        ${Object.entries(this.columns).map((([t,a])=>a.hidden?"":l`
            <div
              role="cell"
              class="mdc-data-table__cell ${b({"mdc-data-table__cell--numeric":"numeric"===a.type,"mdc-data-table__cell--icon":"icon"===a.type,"mdc-data-table__cell--icon-button":"icon-button"===a.type,"mdc-data-table__cell--overflow-menu":"overflow-menu"===a.type,grows:Boolean(a.grows),forceLTR:Boolean(a.forceLTR)})}"
              style=${a.width?m({[a.grows?"minWidth":"width"]:a.width,maxWidth:a.maxWidth?a.maxWidth:""}):""}
            >
              ${a.template?a.template(e[t],e):e[t]}
            </div>
          `))}
      </div>
    `:l``}},{kind:"method",key:"_sortFilterData",value:async function(){const e=(new Date).getTime();this.curRequest++;const t=this.curRequest;let a=this.data;this._filter&&(a=await this._memFilterData(this.data,this._sortColumns,this._filter));const i=this._sortColumn?(async(e,t,a,i)=>(j||(j=S(new Worker(new URL("./sort_filter_worker",import.meta.url)))),j.sortData(e,t,a,i)))(a,this._sortColumns[this._sortColumn],this._sortDirection,this._sortColumn):a,[l]=await Promise.all([i,D]),o=(new Date).getTime()-e;if(o<100&&await new Promise((e=>setTimeout(e,100-o))),this.curRequest===t){if(this.appendRow||this.hasFab){const e=[...l];this.appendRow&&e.push({append:!0,content:this.appendRow}),this.hasFab&&e.push({empty:!0}),this._items=e}else this._items=l;this._filteredData=l}}},{kind:"field",key:"_memFilterData",value:()=>_((async(e,t,a)=>(async(e,t,a)=>(j||(j=S(new Worker(new URL("./sort_filter_worker",import.meta.url)))),j.filterData(e,t,a)))(e,t,a)))},{kind:"method",key:"_handleHeaderClick",value:function(e){const t=e.currentTarget.columnId;this.columns[t].sortable&&(this._sortDirection&&this._sortColumn===t?"asc"===this._sortDirection?this._sortDirection="desc":this._sortDirection=null:this._sortDirection="asc",this._sortColumn=null===this._sortDirection?void 0:t,r(this,"sorting-changed",{column:t,direction:this._sortDirection}))}},{kind:"method",key:"_handleHeaderRowCheckboxClick",value:function(e){e.target.checked?(this._checkedRows=this._filteredData.filter((e=>!1!==e.selectable)).map((e=>e[this.id])),this._checkedRowsChanged()):(this._checkedRows=[],this._checkedRowsChanged())}},{kind:"field",key:"_handleRowCheckboxClick",value(){return e=>{const t=e.currentTarget,a=t.rowId;if(t.checked){if(this._checkedRows.includes(a))return;this._checkedRows=[...this._checkedRows,a]}else this._checkedRows=this._checkedRows.filter((e=>e!==a));this._checkedRowsChanged()}}},{kind:"field",key:"_handleRowClick",value(){return e=>{const t=e.target;if(["HA-CHECKBOX","MWC-BUTTON"].includes(t.tagName))return;const a=e.currentTarget.rowId;r(this,"row-click",{id:a},{bubbles:!1})}}},{kind:"method",key:"_checkedRowsChanged",value:function(){this._items.length&&(this._items=[...this._items]),r(this,"selection-changed",{value:this._checkedRows})}},{kind:"method",key:"_handleSearchChange",value:function(e){this.filter||this._debounceSearch(e.detail.value)}},{kind:"method",key:"_calcTableHeight",value:async function(){this.autoHeight||(await this.updateComplete,this._headerHeight=this._header.clientHeight)}},{kind:"method",decorators:[k({passive:!0})],key:"_saveScrollPos",value:function(e){this._savedScrollPos=e.target.scrollTop}},{kind:"get",static:!0,key:"styles",value:function(){return[g,d`
        /* default mdc styles, colors changed, without checkbox styles */
        :host {
          height: 100%;
        }
        .mdc-data-table__content {
          font-family: Roboto, sans-serif;
          -moz-osx-font-smoothing: grayscale;
          -webkit-font-smoothing: antialiased;
          font-size: 0.875rem;
          line-height: 1.25rem;
          font-weight: 400;
          letter-spacing: 0.0178571429em;
          text-decoration: inherit;
          text-transform: inherit;
        }

        .mdc-data-table {
          background-color: var(--data-table-background-color);
          border-radius: 4px;
          border-width: 1px;
          border-style: solid;
          border-color: var(--divider-color);
          display: inline-flex;
          flex-direction: column;
          box-sizing: border-box;
          overflow: hidden;
        }

        .mdc-data-table__row--selected {
          background-color: rgba(var(--rgb-primary-color), 0.04);
        }

        .mdc-data-table__row {
          display: flex;
          width: 100%;
          height: 52px;
        }

        .mdc-data-table__row ~ .mdc-data-table__row {
          border-top: 1px solid var(--divider-color);
        }

        .mdc-data-table__row:not(.mdc-data-table__row--selected):hover {
          background-color: rgba(var(--rgb-primary-text-color), 0.04);
        }

        .mdc-data-table__header-cell {
          color: var(--primary-text-color);
        }

        .mdc-data-table__cell {
          color: var(--primary-text-color);
        }

        .mdc-data-table__header-row {
          height: 56px;
          display: flex;
          width: 100%;
          border-bottom: 1px solid var(--divider-color);
          overflow-x: auto;
        }

        .mdc-data-table__header-row::-webkit-scrollbar {
          display: none;
        }

        .mdc-data-table__cell,
        .mdc-data-table__header-cell {
          padding-right: 16px;
          padding-left: 16px;
          align-self: center;
          overflow: hidden;
          text-overflow: ellipsis;
          flex-shrink: 0;
          box-sizing: border-box;
        }

        .mdc-data-table__cell.mdc-data-table__cell--icon {
          overflow: initial;
        }

        .mdc-data-table__header-cell--checkbox,
        .mdc-data-table__cell--checkbox {
          /* @noflip */
          padding-left: 16px;
          /* @noflip */
          padding-right: 0;
          width: 60px;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell--checkbox,
        :host([dir="rtl"]) .mdc-data-table__cell--checkbox {
          /* @noflip */
          padding-left: 0;
          /* @noflip */
          padding-right: 16px;
        }

        .mdc-data-table__table {
          height: 100%;
          width: 100%;
          border: 0;
          white-space: nowrap;
        }

        .mdc-data-table__cell {
          font-family: Roboto, sans-serif;
          -moz-osx-font-smoothing: grayscale;
          -webkit-font-smoothing: antialiased;
          font-size: 0.875rem;
          line-height: 1.25rem;
          font-weight: 400;
          letter-spacing: 0.0178571429em;
          text-decoration: inherit;
          text-transform: inherit;
        }

        .mdc-data-table__cell a {
          color: inherit;
          text-decoration: none;
        }

        .mdc-data-table__cell--numeric {
          text-align: right;
        }
        :host([dir="rtl"]) .mdc-data-table__cell--numeric {
          /* @noflip */
          text-align: left;
        }

        .mdc-data-table__cell--icon {
          color: var(--secondary-text-color);
          text-align: center;
        }

        .mdc-data-table__header-cell--icon,
        .mdc-data-table__cell--icon {
          width: 54px;
        }

        .mdc-data-table__header-cell.mdc-data-table__header-cell--icon {
          text-align: center;
        }

        .mdc-data-table__header-cell.sortable.mdc-data-table__header-cell--icon:hover,
        .mdc-data-table__header-cell.sortable.mdc-data-table__header-cell--icon:not(.not-sorted) {
          text-align: left;
        }
        :host([dir="rtl"])
          .mdc-data-table__header-cell.sortable.mdc-data-table__header-cell--icon:hover,
        :host([dir="rtl"])
          .mdc-data-table__header-cell.sortable.mdc-data-table__header-cell--icon:not(.not-sorted) {
          text-align: right;
        }

        .mdc-data-table__cell--icon:first-child ha-icon,
        .mdc-data-table__cell--icon:first-child ha-state-icon,
        .mdc-data-table__cell--icon:first-child ha-svg-icon {
          margin-left: 8px;
        }
        :host([dir="rtl"]) .mdc-data-table__cell--icon:first-child ha-icon,
        :host([dir="rtl"])
          .mdc-data-table__cell--icon:first-child
          ha-state-icon,
        :host([dir="rtl"]) .mdc-data-table__cell--icon:first-child ha-svg-icon {
          margin-left: auto;
          margin-right: 8px;
        }

        .mdc-data-table__cell--icon:first-child state-badge {
          margin-right: -8px;
        }
        :host([dir="rtl"]) .mdc-data-table__cell--icon:first-child state-badge {
          margin-right: auto;
          margin-left: -8px;
        }

        .mdc-data-table__cell--overflow-menu,
        .mdc-data-table__header-cell--overflow-menu,
        .mdc-data-table__header-cell--icon-button,
        .mdc-data-table__cell--icon-button {
          padding: 8px;
        }

        .mdc-data-table__header-cell--icon-button,
        .mdc-data-table__cell--icon-button {
          width: 56px;
        }

        .mdc-data-table__cell--overflow-menu,
        .mdc-data-table__cell--icon-button {
          color: var(--secondary-text-color);
          text-overflow: clip;
        }

        .mdc-data-table__header-cell--icon-button:first-child,
        .mdc-data-table__cell--icon-button:first-child,
        .mdc-data-table__header-cell--icon-button:last-child,
        .mdc-data-table__cell--icon-button:last-child {
          width: 64px;
        }

        .mdc-data-table__cell--overflow-menu:first-child,
        .mdc-data-table__header-cell--overflow-menu:first-child,
        .mdc-data-table__header-cell--icon-button:first-child,
        .mdc-data-table__cell--icon-button:first-child {
          padding-left: 16px;
        }
        :host([dir="rtl"])
          .mdc-data-table__header-cell--overflow-menu:first-child,
        :host([dir="rtl"]) .mdc-data-table__cell--overflow-menu:first-child,
        :host([dir="rtl"])
          .mdc-data-table__header-cell--overflow-menu:first-child,
        :host([dir="rtl"]) .mdc-data-table__cell--overflow-menu:first-child {
          padding-left: 8px;
          padding-right: 16px;
        }

        .mdc-data-table__cell--overflow-menu:last-child,
        .mdc-data-table__header-cell--overflow-menu:last-child,
        .mdc-data-table__header-cell--icon-button:last-child,
        .mdc-data-table__cell--icon-button:last-child {
          padding-right: 16px;
        }
        :host([dir="rtl"])
          .mdc-data-table__header-cell--overflow-menu:last-child,
        :host([dir="rtl"]) .mdc-data-table__cell--overflow-menu:last-child,
        :host([dir="rtl"]) .mdc-data-table__header-cell--icon-button:last-child,
        :host([dir="rtl"]) .mdc-data-table__cell--icon-button:last-child {
          padding-right: 8px;
          padding-left: 16px;
        }
        .mdc-data-table__cell--overflow-menu,
        .mdc-data-table__header-cell--overflow-menu {
          overflow: initial;
        }
        .mdc-data-table__cell--icon-button a {
          color: var(--secondary-text-color);
        }

        .mdc-data-table__header-cell {
          font-family: Roboto, sans-serif;
          -moz-osx-font-smoothing: grayscale;
          -webkit-font-smoothing: antialiased;
          font-size: 0.875rem;
          line-height: 1.375rem;
          font-weight: 500;
          letter-spacing: 0.0071428571em;
          text-decoration: inherit;
          text-transform: inherit;
          text-align: left;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell {
          /* @noflip */
          text-align: right;
        }

        .mdc-data-table__header-cell--numeric {
          text-align: right;
        }
        .mdc-data-table__header-cell--numeric.sortable:hover,
        .mdc-data-table__header-cell--numeric.sortable:not(.not-sorted) {
          text-align: left;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell--numeric {
          /* @noflip */
          text-align: left;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell--numeric.sortable:hover,
        :host([dir="rtl"])
          .mdc-data-table__header-cell--numeric.sortable:not(.not-sorted) {
          text-align: right;
        }

        /* custom from here */

        :host {
          display: block;
        }

        .mdc-data-table {
          display: block;
          border-width: var(--data-table-border-width, 1px);
          height: 100%;
        }
        .mdc-data-table__header-cell {
          overflow: hidden;
          position: relative;
        }
        .mdc-data-table__header-cell span {
          position: relative;
          left: 0px;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell span {
          left: auto;
          right: 0px;
        }

        .mdc-data-table__header-cell.sortable {
          cursor: pointer;
        }
        .mdc-data-table__header-cell > * {
          transition: left 0.2s ease;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell > * {
          transition: right 0.2s ease;
        }
        .mdc-data-table__header-cell ha-svg-icon {
          top: -3px;
          position: absolute;
        }
        .mdc-data-table__header-cell.not-sorted ha-svg-icon {
          left: -20px;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell.not-sorted ha-svg-icon {
          right: -20px;
        }
        .mdc-data-table__header-cell.sortable:not(.not-sorted) span,
        .mdc-data-table__header-cell.sortable.not-sorted:hover span {
          left: 24px;
        }
        :host([dir="rtl"])
          .mdc-data-table__header-cell.sortable:not(.not-sorted)
          span,
        :host([dir="rtl"])
          .mdc-data-table__header-cell.sortable.not-sorted:hover
          span {
          left: auto;
          right: 24px;
        }
        .mdc-data-table__header-cell.sortable:not(.not-sorted) ha-svg-icon,
        .mdc-data-table__header-cell.sortable:hover.not-sorted ha-svg-icon {
          left: 12px;
        }
        :host([dir="rtl"])
          .mdc-data-table__header-cell.sortable:not(.not-sorted)
          ha-svg-icon,
        :host([dir="rtl"])
          .mdc-data-table__header-cell.sortable:hover.not-sorted
          ha-svg-icon {
          left: auto;
          right: 12px;
        }
        .table-header {
          border-bottom: 1px solid var(--divider-color);
        }
        search-input {
          display: block;
          flex: 1;
        }
        slot[name="header"] {
          display: block;
        }
        .center {
          text-align: center;
        }
        .secondary {
          color: var(--secondary-text-color);
        }
        .scroller {
          height: calc(100% - 57px);
          overflow: overlay !important;
        }

        .mdc-data-table__table.auto-height .scroller {
          overflow-y: hidden !important;
        }
        .grows {
          flex-grow: 1;
          flex-shrink: 1;
        }
        .forceLTR {
          direction: ltr;
        }
        .clickable {
          cursor: pointer;
        }
        lit-virtualizer {
          contain: size layout !important;
        }
      `]}}]}}),t),e([s("ha-tab")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[a({type:Boolean,reflect:!0})],key:"active",value:()=>!1},{kind:"field",decorators:[a({type:Boolean,reflect:!0})],key:"narrow",value:()=>!1},{kind:"field",decorators:[a()],key:"name",value:void 0},{kind:"field",decorators:[y("mwc-ripple")],key:"_ripple",value:void 0},{kind:"field",decorators:[i()],key:"_shouldRenderRipple",value:()=>!1},{kind:"method",key:"render",value:function(){return l`
      <div
        tabindex="0"
        role="tab"
        aria-selected=${this.active}
        aria-label=${p(this.name)}
        @focus=${this.handleRippleFocus}
        @blur=${this.handleRippleBlur}
        @mousedown=${this.handleRippleActivate}
        @mouseup=${this.handleRippleDeactivate}
        @mouseenter=${this.handleRippleMouseEnter}
        @mouseleave=${this.handleRippleMouseLeave}
        @touchstart=${this.handleRippleActivate}
        @touchend=${this.handleRippleDeactivate}
        @touchcancel=${this.handleRippleDeactivate}
        @keydown=${this._handleKeyDown}
      >
        ${this.narrow?l`<slot name="icon"></slot>`:""}
        <span class="name">${this.name}</span>
        ${this._shouldRenderRipple?l`<mwc-ripple></mwc-ripple>`:""}
      </div>
    `}},{kind:"field",key:"_rippleHandlers",value(){return new w((()=>(this._shouldRenderRipple=!0,this._ripple)))}},{kind:"method",key:"_handleKeyDown",value:function(e){13===e.keyCode&&e.target.click()}},{kind:"method",decorators:[k({passive:!0})],key:"handleRippleActivate",value:function(e){this._rippleHandlers.startPress(e)}},{kind:"method",key:"handleRippleDeactivate",value:function(){this._rippleHandlers.endPress()}},{kind:"method",key:"handleRippleMouseEnter",value:function(){this._rippleHandlers.startHover()}},{kind:"method",key:"handleRippleMouseLeave",value:function(){this._rippleHandlers.endHover()}},{kind:"method",key:"handleRippleFocus",value:function(){this._rippleHandlers.startFocus()}},{kind:"method",key:"handleRippleBlur",value:function(){this._rippleHandlers.endFocus()}},{kind:"get",static:!0,key:"styles",value:function(){return d`
      div {
        padding: 0 32px;
        display: flex;
        flex-direction: column;
        text-align: center;
        box-sizing: border-box;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: var(--header-height);
        cursor: pointer;
        position: relative;
        outline: none;
      }

      .name {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 100%;
      }

      :host([active]) {
        color: var(--primary-color);
      }

      :host(:not([narrow])[active]) div {
        border-bottom: 2px solid var(--primary-color);
      }

      :host([narrow]) {
        min-width: 0;
        display: flex;
        justify-content: center;
        overflow: hidden;
      }

      :host([narrow]) div {
        padding: 0 4px;
      }
    `}}]}}),t),e([s("hass-tabs-subpage")],(function(e,t){class o extends t{constructor(...t){super(...t),e(this)}}return{F:o,d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a({type:Boolean})],key:"supervisor",value:()=>!1},{kind:"field",decorators:[a({attribute:!1})],key:"localizeFunc",value:void 0},{kind:"field",decorators:[a({type:String,attribute:"back-path"})],key:"backPath",value:void 0},{kind:"field",decorators:[a()],key:"backCallback",value:void 0},{kind:"field",decorators:[a({type:Boolean,attribute:"main-page"})],key:"mainPage",value:()=>!1},{kind:"field",decorators:[a({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[a({attribute:!1})],key:"tabs",value:void 0},{kind:"field",decorators:[a({type:Boolean,reflect:!0})],key:"narrow",value:()=>!1},{kind:"field",decorators:[a({type:Boolean,reflect:!0,attribute:"is-wide"})],key:"isWide",value:()=>!1},{kind:"field",decorators:[a({type:Boolean,reflect:!0})],key:"rtl",value:()=>!1},{kind:"field",decorators:[i()],key:"_activeTab",value:void 0},{kind:"field",decorators:[R(".content")],key:"_savedScrollPos",value:void 0},{kind:"field",key:"_getTabs",value(){return _(((e,t,a,i,o,r,d)=>e.filter((e=>(!e.component||e.core||T(this.hass,e.component))&&(!e.advancedOnly||a))).map((e=>l`
            <a href=${e.path}>
              <ha-tab
                .hass=${this.hass}
                .active=${e.path===(null==t?void 0:t.path)}
                .narrow=${this.narrow}
                .name=${e.translationKey?d(e.translationKey):e.name}
              >
                ${e.iconPath?l`<ha-svg-icon
                      slot="icon"
                      .path=${e.iconPath}
                    ></ha-svg-icon>`:""}
              </ha-tab>
            </a>
          `))))}},{kind:"method",key:"willUpdate",value:function(e){if(e.has("route")&&(this._activeTab=this.tabs.find((e=>`${this.route.prefix}${this.route.path}`.includes(e.path)))),e.has("hass")){const t=e.get("hass");t&&t.language===this.hass.language||(this.rtl=z(this.hass))}h(u(o.prototype),"willUpdate",this).call(this,e)}},{kind:"method",key:"render",value:function(){var e,t;const a=this._getTabs(this.tabs,this._activeTab,null===(e=this.hass.userData)||void 0===e?void 0:e.showAdvanced,this.hass.config.components,this.hass.language,this.narrow,this.localizeFunc||this.hass.localize),i=a.length>1||!this.narrow;return l`
      <div class="toolbar">
        ${this.mainPage||!this.backPath&&null!==(t=history.state)&&void 0!==t&&t.root?l`
              <ha-menu-button
                .hassio=${this.supervisor}
                .hass=${this.hass}
                .narrow=${this.narrow}
              ></ha-menu-button>
            `:this.backPath?l`
              <a href=${this.backPath}>
                <ha-icon-button-arrow-prev
                  .hass=${this.hass}
                ></ha-icon-button-arrow-prev>
              </a>
            `:l`
              <ha-icon-button-arrow-prev
                .hass=${this.hass}
                @click=${this._backTapped}
              ></ha-icon-button-arrow-prev>
            `}
        ${this.narrow?l`<div class="main-title"><slot name="header"></slot></div>`:""}
        ${i?l`
              <div id="tabbar" class=${b({"bottom-bar":this.narrow})}>
                ${a}
              </div>
            `:""}
        <div id="toolbar-icon">
          <slot name="toolbar-icon"></slot>
        </div>
      </div>
      <div
        class="content ${b({tabs:i})}"
        @scroll=${this._saveScrollPos}
      >
        <slot></slot>
      </div>
      <div id="fab" class=${b({tabs:i})}>
        <slot name="fab"></slot>
      </div>
    `}},{kind:"method",decorators:[k({passive:!0})],key:"_saveScrollPos",value:function(e){this._savedScrollPos=e.target.scrollTop}},{kind:"method",key:"_backTapped",value:function(){this.backCallback?this.backCallback():history.back()}},{kind:"get",static:!0,key:"styles",value:function(){return d`
      :host {
        display: block;
        height: 100%;
        background-color: var(--primary-background-color);
      }

      :host([narrow]) {
        width: 100%;
        position: fixed;
      }

      ha-menu-button {
        margin-right: 24px;
      }

      .toolbar {
        display: flex;
        align-items: center;
        font-size: 20px;
        height: var(--header-height);
        background-color: var(--sidebar-background-color);
        font-weight: 400;
        border-bottom: 1px solid var(--divider-color);
        padding: 0 16px;
        box-sizing: border-box;
      }
      .toolbar a {
        color: var(--sidebar-text-color);
        text-decoration: none;
      }
      .bottom-bar a {
        width: 25%;
      }

      #tabbar {
        display: flex;
        font-size: 14px;
        overflow: hidden;
      }

      #tabbar > a {
        overflow: hidden;
        max-width: 45%;
      }

      #tabbar.bottom-bar {
        position: absolute;
        bottom: 0;
        left: 0;
        padding: 0 16px;
        box-sizing: border-box;
        background-color: var(--sidebar-background-color);
        border-top: 1px solid var(--divider-color);
        justify-content: space-around;
        z-index: 2;
        font-size: 12px;
        width: 100%;
        padding-bottom: env(safe-area-inset-bottom);
      }

      #tabbar:not(.bottom-bar) {
        flex: 1;
        justify-content: center;
      }

      :host(:not([narrow])) #toolbar-icon {
        min-width: 40px;
      }

      ha-menu-button,
      ha-icon-button-arrow-prev,
      ::slotted([slot="toolbar-icon"]) {
        display: flex;
        flex-shrink: 0;
        pointer-events: auto;
        color: var(--sidebar-icon-color);
      }

      .main-title {
        flex: 1;
        max-height: var(--header-height);
        line-height: 20px;
        color: var(--sidebar-text-color);
      }

      .content {
        position: relative;
        width: calc(
          100% - env(safe-area-inset-left) - env(safe-area-inset-right)
        );
        margin-left: env(safe-area-inset-left);
        margin-right: env(safe-area-inset-right);
        height: calc(100% - 1px - var(--header-height));
        height: calc(
          100% - 1px - var(--header-height) - env(safe-area-inset-bottom)
        );
        overflow: auto;
        -webkit-overflow-scrolling: touch;
      }

      :host([narrow]) .content.tabs {
        height: calc(100% - 2 * var(--header-height));
        height: calc(
          100% - 2 * var(--header-height) - env(safe-area-inset-bottom)
        );
      }

      #fab {
        position: fixed;
        right: calc(16px + env(safe-area-inset-right));
        bottom: calc(16px + env(safe-area-inset-bottom));
        z-index: 1;
      }
      :host([narrow]) #fab.tabs {
        bottom: calc(84px + env(safe-area-inset-bottom));
      }
      #fab[is-wide] {
        bottom: 24px;
        right: 24px;
      }
      :host([rtl]) #fab {
        right: auto;
        left: calc(16px + env(safe-area-inset-left));
      }
      :host([rtl][is-wide]) #fab {
        bottom: 24px;
        left: 24px;
        right: auto;
      }
    `}}]}}),t),e([s("hass-tabs-subpage-data-table")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a({attribute:!1})],key:"localizeFunc",value:void 0},{kind:"field",decorators:[a({type:Boolean})],key:"isWide",value:()=>!1},{kind:"field",decorators:[a({type:Boolean,reflect:!0})],key:"narrow",value:()=>!1},{kind:"field",decorators:[a({type:Boolean})],key:"supervisor",value:()=>!1},{kind:"field",decorators:[a({type:Boolean,attribute:"main-page"})],key:"mainPage",value:()=>!1},{kind:"field",decorators:[a({type:Object})],key:"columns",value:()=>({})},{kind:"field",decorators:[a({type:Array})],key:"data",value:()=>[]},{kind:"field",decorators:[a({type:Boolean})],key:"selectable",value:()=>!1},{kind:"field",decorators:[a({type:Boolean})],key:"clickable",value:()=>!1},{kind:"field",decorators:[a({type:Boolean})],key:"hasFab",value:()=>!1},{kind:"field",decorators:[a({attribute:!1})],key:"appendRow",value:void 0},{kind:"field",decorators:[a({type:String})],key:"id",value:()=>"id"},{kind:"field",decorators:[a({type:String})],key:"filter",value:()=>""},{kind:"field",decorators:[a()],key:"searchLabel",value:void 0},{kind:"field",decorators:[a({type:Array})],key:"activeFilters",value:void 0},{kind:"field",decorators:[a()],key:"hiddenLabel",value:void 0},{kind:"field",decorators:[a({type:Number})],key:"numHidden",value:()=>0},{kind:"field",decorators:[a({type:String,attribute:"back-path"})],key:"backPath",value:void 0},{kind:"field",decorators:[a()],key:"backCallback",value:void 0},{kind:"field",decorators:[a({type:String})],key:"noDataText",value:void 0},{kind:"field",decorators:[a()],key:"route",value:void 0},{kind:"field",decorators:[a()],key:"tabs",value:void 0},{kind:"field",decorators:[a({type:Boolean})],key:"hideFilterMenu",value:()=>!1},{kind:"field",decorators:[c("ha-data-table",!0)],key:"_dataTable",value:void 0},{kind:"method",key:"clearSelection",value:function(){this._dataTable.clearSelection()}},{kind:"method",key:"render",value:function(){const e=this.numHidden?this.hiddenLabel||this.hass.localize("ui.components.data-table.hidden","number",this.numHidden)||this.numHidden:void 0,t=this.activeFilters?l`${this.hass.localize("ui.components.data-table.filtering_by")}
        ${this.activeFilters.join(", ")}
        ${e?`(${e})`:""}`:e,a=l`<search-input
      .hass=${this.hass}
      .filter=${this.filter}
      .suffix=${!this.narrow}
      @value-changed=${this._handleSearchChange}
      .label=${this.searchLabel||this.hass.localize("ui.components.data-table.search")}
    >
      ${this.narrow?"":l`<div
            class="filters"
            slot="suffix"
            @click=${this._preventDefault}
          >
            ${t?l`<div class="active-filters">
                  ${t}
                  <mwc-button @click=${this._clearFilter}>
                    ${this.hass.localize("ui.components.data-table.clear")}
                  </mwc-button>
                </div>`:""}
            <slot name="filter-menu"></slot>
          </div>`}
    </search-input>`;return l`
      <hass-tabs-subpage
        .hass=${this.hass}
        .localizeFunc=${this.localizeFunc}
        .narrow=${this.narrow}
        .isWide=${this.isWide}
        .backPath=${this.backPath}
        .backCallback=${this.backCallback}
        .route=${this.route}
        .tabs=${this.tabs}
        .mainPage=${this.mainPage}
        .supervisor=${this.supervisor}
      >
        ${this.hideFilterMenu?"":l`
              <div slot="toolbar-icon">
                ${this.narrow?l`
                      <div class="filter-menu">
                        ${this.numHidden||this.activeFilters?l`<span class="badge"
                              >${this.numHidden||"!"}</span
                            >`:""}
                        <slot name="filter-menu"></slot>
                      </div>
                    `:""}<slot name="toolbar-icon"></slot>
              </div>
            `}
        ${this.narrow?l`
              <div slot="header">
                <slot name="header">
                  <div class="search-toolbar">${a}</div>
                </slot>
              </div>
            `:""}
        <ha-data-table
          .hass=${this.hass}
          .columns=${this.columns}
          .data=${this.data}
          .filter=${this.filter}
          .selectable=${this.selectable}
          .hasFab=${this.hasFab}
          .id=${this.id}
          .noDataText=${this.noDataText}
          .dir=${P(this.hass)}
          .clickable=${this.clickable}
          .appendRow=${this.appendRow}
        >
          ${this.narrow?l` <div slot="header"></div> `:l`
                <div slot="header">
                  <slot name="header">
                    <div class="table-header">${a}</div>
                  </slot>
                </div>
              `}
        </ha-data-table>
        <div slot="fab"><slot name="fab"></slot></div>
      </hass-tabs-subpage>
    `}},{kind:"method",key:"_preventDefault",value:function(e){e.preventDefault()}},{kind:"method",key:"_handleSearchChange",value:function(e){this.filter!==e.detail.value&&(this.filter=e.detail.value,r(this,"search-changed",{value:this.filter}))}},{kind:"method",key:"_clearFilter",value:function(){r(this,"clear-filter")}},{kind:"get",static:!0,key:"styles",value:function(){return d`
      ha-data-table {
        width: 100%;
        height: 100%;
        --data-table-border-width: 0;
      }
      :host(:not([narrow])) ha-data-table {
        height: calc(100vh - 1px - var(--header-height));
        display: block;
      }
      .table-header {
        display: flex;
        align-items: center;
        --mdc-shape-small: 0;
        height: 56px;
      }
      .search-toolbar {
        display: flex;
        align-items: center;
        color: var(--secondary-text-color);
      }
      search-input {
        --mdc-text-field-fill-color: var(--sidebar-background-color);
        --mdc-text-field-idle-line-color: var(--divider-color);
        --text-field-overflow: visible;
        z-index: 5;
      }
      .table-header search-input {
        display: block;
        position: absolute;
        top: 0;
        right: 0;
        left: 0;
      }
      .search-toolbar search-input {
        display: block;
        width: 100%;
        color: var(--secondary-text-color);
        --mdc-ripple-color: transparant;
      }
      .filters {
        --mdc-text-field-fill-color: var(--input-fill-color);
        --mdc-text-field-idle-line-color: var(--input-idle-line-color);
        --mdc-shape-small: 4px;
        --text-field-overflow: initial;
        display: flex;
        justify-content: flex-end;
        margin-right: 8px;
        color: var(--primary-text-color);
      }
      .active-filters {
        color: var(--primary-text-color);
        position: relative;
        display: flex;
        align-items: center;
        padding: 2px 2px 2px 8px;
        margin-left: 4px;
        font-size: 14px;
        width: max-content;
        cursor: initial;
      }
      .active-filters ha-svg-icon {
        color: var(--primary-color);
      }
      .active-filters mwc-button {
        margin-left: 8px;
      }
      .active-filters::before {
        background-color: var(--primary-color);
        opacity: 0.12;
        border-radius: 4px;
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        content: "";
      }
      .badge {
        min-width: 20px;
        box-sizing: border-box;
        border-radius: 50%;
        font-weight: 400;
        background-color: var(--primary-color);
        line-height: 20px;
        text-align: center;
        padding: 0px 4px;
        color: var(--text-primary-color);
        position: absolute;
        right: 0;
        top: 4px;
        font-size: 0.65em;
      }
      .filter-menu {
        position: relative;
      }
    `}}]}}),t);
