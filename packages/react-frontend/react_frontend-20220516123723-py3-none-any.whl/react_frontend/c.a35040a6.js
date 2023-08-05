import{ar as r}from"./main-ac83c92b.js";import{bg as t,a$ as a}from"./c.3e14cfd3.js";import"./c.027db416.js";import"./c.8cbd7110.js";customElements.define("hui-vertical-stack-card",class extends t{async getCardSize(){if(!this._cards)return 0;const r=[];for(const t of this._cards)r.push(a(t));return(await Promise.all(r)).reduce(((r,t)=>r+t),0)}static get styles(){return[super.sharedStyles,r`
        #root {
          display: flex;
          flex-direction: column;
          height: 100%;
        }
        #root > * {
          margin: var(
            --vertical-stack-card-margin,
            var(--stack-card-margin, 4px 0)
          );
        }
        #root > *:first-child {
          margin-top: 0;
        }
        #root > *:last-child {
          margin-bottom: 0;
        }
      `]}});
