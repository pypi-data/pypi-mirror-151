import{an as e,n as t,ap as s,e as i,$ as c,aq as a,ar as h,_ as o}from"./main-ac83c92b.js";import{s as r,C as d}from"./c.47fa9be3.js";import{ao as n,ap as p}from"./c.027db416.js";let l=class extends d{};l.styles=[r],l=e([t("mwc-checkbox")],l);class m extends n{constructor(){super(...arguments),this.left=!1,this.graphic="control"}render(){const e={"mdc-deprecated-list-item__graphic":this.left,"mdc-deprecated-list-item__meta":!this.left},t=this.renderText(),s=this.graphic&&"control"!==this.graphic&&!this.left?this.renderGraphic():c``,i=this.hasMeta&&this.left?this.renderMeta():c``,h=this.renderRipple();return c`
      ${h}
      ${s}
      ${this.left?"":t}
      <span class=${a(e)}>
        <mwc-checkbox
            reducedTouchTarget
            tabindex=${this.tabindex}
            .checked=${this.selected}
            ?disabled=${this.disabled}
            @change=${this.onChange}>
        </mwc-checkbox>
      </span>
      ${this.left?t:""}
      ${i}`}async onChange(e){const t=e.target;this.selected===t.checked||(this._skipPropRequest=!0,this.selected=t.checked,await this.updateComplete,this._skipPropRequest=!1)}}e([s("slot")],m.prototype,"slotElement",void 0),e([s("mwc-checkbox")],m.prototype,"checkboxElement",void 0),e([i({type:Boolean})],m.prototype,"left",void 0),e([i({type:String,reflect:!0})],m.prototype,"graphic",void 0);const f=h`:host(:not([twoline])){height:56px}:host(:not([left])) .mdc-deprecated-list-item__meta{height:40px;width:40px}`;o([t("ha-check-list-item")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",static:!0,key:"styles",value:()=>[p,f,h`
      :host {
        --mdc-theme-secondary: var(--primary-color);
      }
    `]}]}}),m);
