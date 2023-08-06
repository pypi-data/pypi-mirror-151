import{a as i,V as t,e,m as o,$ as s,n as r}from"./main-e088bb19.js";import{m as a}from"./c.73230ac7.js";import"./c.14628ea3.js";import"./c.3c6412dd.js";import"./c.743a15a1.js";import"./c.7943fa91.js";import"./c.8e28b461.js";import"./c.166c4b5c.js";let d=i([r("vais-generic-dialog")],(function(i,t){return{F:class extends t{constructor(...t){super(...t),i(this)}},d:[{kind:"field",decorators:[e({type:Boolean})],key:"markdown",value:()=>!1},{kind:"field",decorators:[e()],key:"repository",value:void 0},{kind:"field",decorators:[e()],key:"header",value:void 0},{kind:"field",decorators:[e()],key:"content",value:void 0},{kind:"field",key:"_getRepository",value:()=>o(((i,t)=>null==i?void 0:i.find((i=>i.id===t))))},{kind:"method",key:"render",value:function(){if(!this.active||!this.repository)return s``;const i=this._getRepository(this.vais.repositories,this.repository);return s`
      <vais-dialog .active=${this.active} .narrow=${this.narrow} .hass=${this.hass}>
        <div slot="header">${this.header||""}</div>
        ${this.markdown?this.repository?a.html(this.content||"",i):a.html(this.content||""):this.content||""}
      </vais-dialog>
    `}}]}}),t);export{d as VaisGenericDialog};
