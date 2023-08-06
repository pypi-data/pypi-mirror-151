import{a as i,V as s,e as t,$ as e,d as a,r as o,ar as r,as as l,ao as n,at as c,au as d,n as v}from"./main-e088bb19.js";import"./c.14628ea3.js";import"./c.7943fa91.js";import"./c.8e28b461.js";import"./c.166c4b5c.js";let h=i([v("vais-removed-dialog")],(function(i,s){return{F:class extends s{constructor(...s){super(...s),i(this)}},d:[{kind:"field",decorators:[t({attribute:!1})],key:"repository",value:void 0},{kind:"field",decorators:[t({type:Boolean})],key:"_updating",value:()=>!1},{kind:"method",key:"render",value:function(){if(!this.active)return e``;const i=this.vais.removed.find((i=>i.repository===this.repository.full_name));return e`
      <vais-dialog
        .active=${this.active}
        .hass=${this.hass}
        .title=${this.vais.localize("entry.messages.removed_repository",{repository:this.repository.full_name})}
      >
        <div class="content">
          <div><b>${this.vais.localize("dialog_removed.name")}:</b> ${this.repository.name}</div>
          ${i.removal_type?e` <div>
                <b>${this.vais.localize("dialog_removed.type")}:</b> ${i.removal_type}
              </div>`:""}
          ${i.reason?e` <div>
                <b>${this.vais.localize("dialog_removed.reason")}:</b> ${i.reason}
              </div>`:""}
          ${i.link?e`          <div>
            </b><vais-link .url=${i.link}>${this.vais.localize("dialog_removed.link")}</vais-link>
          </div>`:""}
        </div>
        <mwc-button slot="secondaryaction" @click=${this._ignoreRepository}>
          ${this.vais.localize("common.ignore")}
        </mwc-button>
        <mwc-button class="uninstall" slot="primaryaction" @click=${this._uninstallRepository}
          >${this._updating?e`<ha-circular-progress active size="small"></ha-circular-progress>`:this.vais.localize("common.remove")}</mwc-button
        >
      </vais-dialog>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[a,o`
        .uninstall {
          --mdc-theme-primary: var(--hcv-color-error);
        }
      `]}},{kind:"method",key:"_lovelaceUrl",value:function(){var i,s;return`/vaisfiles/${null===(i=this.repository)||void 0===i?void 0:i.full_name.split("/")[1]}/${null===(s=this.repository)||void 0===s?void 0:s.file_name}`}},{kind:"method",key:"_ignoreRepository",value:async function(){await r(this.hass,this.repository.full_name);const i=await l(this.hass);this.dispatchEvent(new CustomEvent("update-vais",{detail:{removed:i},bubbles:!0,composed:!0})),this.dispatchEvent(new Event("vais-dialog-closed",{bubbles:!0,composed:!0}))}},{kind:"method",key:"_uninstallRepository",value:async function(){if(this._updating=!0,"plugin"===this.repository.category&&this.vais.status&&"yaml"!==this.vais.status.lovelace_mode){(await n(this.hass)).filter((i=>i.url===this._lovelaceUrl())).forEach((i=>{c(this.hass,String(i.id))}))}await d(this.hass,this.repository.id),this._updating=!1,this.active=!1}}]}}),s);export{h as VaisRemovedDialog};
