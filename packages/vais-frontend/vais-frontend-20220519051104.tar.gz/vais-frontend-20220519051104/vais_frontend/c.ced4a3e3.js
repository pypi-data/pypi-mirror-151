import{a as i,V as e,e as t,$ as s,n as o}from"./main-e088bb19.js";import"./c.14628ea3.js";import"./c.7943fa91.js";import"./c.8e28b461.js";import"./c.166c4b5c.js";let c=i([o("vais-progress-dialog")],(function(i,e){return{F:class extends e{constructor(...e){super(...e),i(this)}},d:[{kind:"field",decorators:[t()],key:"title",value:void 0},{kind:"field",decorators:[t()],key:"content",value:void 0},{kind:"field",decorators:[t()],key:"confirmText",value:void 0},{kind:"field",decorators:[t()],key:"confirm",value:void 0},{kind:"field",decorators:[t({type:Boolean})],key:"_inProgress",value:()=>!1},{kind:"method",key:"shouldUpdate",value:function(i){return i.has("active")||i.has("title")||i.has("content")||i.has("confirmText")||i.has("confirm")||i.has("_inProgress")}},{kind:"method",key:"render",value:function(){return this.active?s`
      <vais-dialog .active=${this.active} .hass=${this.hass} title=${this.title||""}>
        <div class="content">
          ${this.content||""}
        </div>
        <mwc-button slot="secondaryaction" ?disabled=${this._inProgress} @click=${this._close}>
          ${this.vais.localize("common.cancel")}
        </mwc-button>
        <mwc-button slot="primaryaction" @click=${this._confirmed}>
          ${this._inProgress?s`<ha-circular-progress active size="small"></ha-circular-progress>`:this.confirmText||this.vais.localize("common.yes")}</mwc-button
          >
        </mwc-button>
      </vais-dialog>
    `:s``}},{kind:"method",key:"_confirmed",value:async function(){this._inProgress=!0,await this.confirm(),this._inProgress=!1,this._close()}},{kind:"method",key:"_close",value:function(){this.active=!1,this.dispatchEvent(new Event("vais-dialog-closed",{bubbles:!0,composed:!0}))}}]}}),e);export{c as VaisProgressDialog};
