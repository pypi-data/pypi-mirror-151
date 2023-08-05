import{_ as e,s as t,e as i,t as a,m as s,$ as r,r as o,f as d,h as n,n as l,H as c,g as h,i as u}from"./main-ac83c92b.js";import{c as f,f as v,d as k,a as p}from"./c.027db416.js";import"./c.3e573ea1.js";import"./c.d76504d5.js";import"./c.39da0aeb.js";import"./c.cfa85e17.js";import"./c.5b2e0d05.js";import"./c.be47aa9a.js";import"./c.02ed471c.js";import"./c.0e001851.js";import"./c.53212acc.js";import"./c.4860f91b.js";import"./c.e9aa747b.js";import"./c.0660f3f3.js";import"./c.c8193d47.js";import"./c.47fa9be3.js";import"./c.d2605417.js";e([l("react-reaction-panel")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[i()],key:"route",value:void 0},{kind:"field",decorators:[i()],key:"reactions",value:void 0},{kind:"field",decorators:[i()],key:"_activeFilters",value:void 0},{kind:"field",decorators:[a()],key:"_filteredReactions",value:void 0},{kind:"field",decorators:[a()],key:"_filterValue",value:void 0},{kind:"field",key:"_reactions",value:()=>s(((e,t)=>null===t?[]:(t?e.filter((e=>t.includes(e.entity_id))):e).map((e=>({...e,name:f(e),last_triggered:e.attributes.last_triggered||void 0})))))},{kind:"field",key:"_columns",value(){return s(((e,t)=>({toggle:{title:"",label:this.hass.localize("ui.panel.config.reaction.picker.headers.toggle"),type:"icon",template:(e,t)=>r`
                        <ha-entity-toggle
                        .hass=${this.hass}
                        .stateObj=${t}
                        ></ha-entity-toggle>
                    `},name:{title:this.hass.localize("ui.panel.config.reaction.picker.headers.name"),sortable:!0,filterable:!0,direction:"asc",grows:!0,template:e?(e,t)=>r`
                            ${e}
                            <div class="secondary">
                            ${this.hass.localize("ui.card.reaction.last_triggered")}:
                            ${t.attributes.last_triggered?v(new Date(t.attributes.last_triggered),this.hass.locale):this.hass.localize("ui.components.relative_time.never")}
                            </div>
                        `:void 0}})))}},{kind:"method",key:"render",value:function(){return r`
        <hass-tabs-subpage-data-table
            .hass=${this.hass}
            .narrow=${this.narrow}
            back-path="/react"
            id="id"
            .route=${this.route}
            .tabs=${o.react}
            .activeFilters=${this._activeFilters}
            .columns=${this._columns(this.narrow,this.hass.locale)}
            .data=${this._reactions(this.reactions,this._filteredReactions)}
            .noDataText=${this.hass.localize("ui.panel.config.reaction.picker.no_reactions")}
            @clear-filter=${this._clearFilter}
            hasFab
        >
            <ha-button-related-filter-menu
                slot="filter-menu"
                corner="BOTTOM_START"
                .narrow=${this.narrow}
                .hass=${this.hass}
                .value=${this._filterValue}
                exclude-domains='["reaction"]'
                @related-changed=${this._relatedFilterChanged}
            >
            </ha-button-related-filter-menu>
        </hass-tabs-subpage-data-table>
      `}},{kind:"method",key:"_relatedFilterChanged",value:function(e){this._filterValue=e.detail.value,this._filterValue?(this._activeFilters=[e.detail.filter],this._filteredReactions=e.detail.items.reaction||null):this._clearFilter()}},{kind:"method",key:"_clearFilter",value:function(){this._filteredReactions=void 0,this._activeFilters=void 0,this._filterValue=void 0}},{kind:"method",key:"_showInfo",value:function(e){const t=e.entity_id;d(this,"hass-more-info",{entityId:t})}},{kind:"field",key:"_triggerRunActions",value(){return e=>{this._runActions(e.currentTarget.reaction)}}},{kind:"field",key:"_runActions",value:()=>e=>{}},{kind:"get",static:!0,key:"styles",value:function(){return n}}]}}),t);e([l("react-reaction-router")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"narrow",value:void 0},{kind:"field",decorators:[i()],key:"isWide",value:void 0},{kind:"field",decorators:[i()],key:"showAdvanced",value:void 0},{kind:"field",decorators:[i()],key:"reactions",value:()=>[]},{kind:"field",key:"_debouncedUpdateReactions",value(){return k((e=>{const t=this._getReactions(this.hass.states);var i,a;i=t,a=e.reactions,i.length===a.length&&i.every(((e,t)=>e===a[t]))||(e.reactions=t)}),10)}},{kind:"field",key:"routerOptions",value:()=>({defaultPage:"dashboard",routes:{dashboard:{tag:"react-reaction-panel",cache:!0}}})},{kind:"field",key:"_getReactions",value:()=>s((e=>Object.values(e).filter((e=>"react"===p(e)&&!e.attributes.restored))))},{kind:"method",key:"firstUpdated",value:function(e){h(u(a.prototype),"firstUpdated",this).call(this,e)}},{kind:"method",key:"updatePageEl",value:function(e,t){if(e.hass=this.hass,e.narrow=this.narrow,e.isWide=this.isWide,e.route=this.routeTail,e.showAdvanced=this.showAdvanced,this.hass&&(e.reactions&&t?t.has("hass")&&this._debouncedUpdateReactions(e):e.reactions=this._getReactions(this.hass.states)),(!t||t.has("route"))&&"dashboard"!==this._currentPage){const t=decodeURIComponent(this.routeTail.path.substr(1));e.reactionId="new"===t?null:t}}}]}}),c);
