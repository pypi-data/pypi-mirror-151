import{ar as r}from"./main-ac83c92b.js";import{bg as t,a$ as a}from"./c.3e14cfd3.js";import"./c.027db416.js";import"./c.8cbd7110.js";customElements.define("hui-horizontal-stack-card",class extends t{async getCardSize(){if(!this._cards)return 0;const r=[];for(const t of this._cards)r.push(a(t));const t=await Promise.all(r);return Math.max(...t)}static get styles(){return[super.sharedStyles,r`
        #root {
          display: flex;
          height: 100%;
        }
        #root > * {
          flex: 1 1 0;
          margin: var(
            --horizontal-stack-card-margin,
            var(--stack-card-margin, 0 4px)
          );
          min-width: 0;
        }
        #root > *:first-child {
          margin-left: 0;
        }
        #root > *:last-child {
          margin-right: 0;
        }
      `]}});
