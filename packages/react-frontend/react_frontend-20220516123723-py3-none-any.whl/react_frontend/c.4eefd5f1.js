import{eE as t,_ as e,s as r,e as i,g as n,i as o,$ as a,ar as s,n as u,t as c,ap as l,aq as h,aA as d,cu as f,dW as p,di as g,f as m}from"./main-ac83c92b.js";import"./c.a4895d0e.js";import{a2 as _,a3 as v,U as b,z as y,c as k,d as w}from"./c.027db416.js";import{aG as x,aJ as M,bj as C,B as O,bk as D,bl as L,D as P,bm as S,aH as T,O as j,N as I,bn as q}from"./c.3e14cfd3.js";import{s as z}from"./c.6999bfff.js";import"./c.8cbd7110.js";var V=_((function(t,e){var r;window,r=function(){return function(t){var e={};function r(i){if(e[i])return e[i].exports;var n=e[i]={i:i,l:!1,exports:{}};return t[i].call(n.exports,n,n.exports,r),n.l=!0,n.exports}return r.m=t,r.c=e,r.d=function(t,e,i){r.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:i})},r.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},r.t=function(t,e){if(1&e&&(t=r(t)),8&e)return t;if(4&e&&"object"==typeof t&&t&&t.__esModule)return t;var i=Object.create(null);if(r.r(i),Object.defineProperty(i,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var n in t)r.d(i,n,function(e){return t[e]}.bind(null,n));return i},r.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return r.d(e,"a",e),e},r.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},r.p="",r(r.s=10)}([function(t,e,r){Object.defineProperty(e,"__esModule",{value:!0}),e.assignDeep=e.mapValues=void 0,e.mapValues=function(t,e){var r={};for(var i in t)if(t.hasOwnProperty(i)){var n=t[i];r[i]=e(n)}return r},e.assignDeep=function t(e){for(var r=[],i=1;i<arguments.length;i++)r[i-1]=arguments[i];return r.forEach((function(r){if(r)for(var i in r)if(r.hasOwnProperty(i)){var n=r[i];Array.isArray(n)?e[i]=n.slice(0):"object"==typeof n?(e[i]||(e[i]={}),t(e[i],n)):e[i]=n}})),e}},function(t,e,r){var i=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}};Object.defineProperty(e,"__esModule",{value:!0});var n=r(7),o=i(r(8)),a=r(0),s=function(){function t(e,r){this._src=e,this.opts=a.assignDeep({},t.DefaultOpts,r)}return t.use=function(t){this._pipeline=t},t.from=function(t){return new o.default(t)},Object.defineProperty(t.prototype,"result",{get:function(){return this._result},enumerable:!1,configurable:!0}),t.prototype._process=function(e,r){this.opts.quantizer,e.scaleDown(this.opts);var i=n.buildProcessOptions(this.opts,r);return t._pipeline.process(e.getImageData(),i)},t.prototype.palette=function(){return this.swatches()},t.prototype.swatches=function(){throw new Error("Method deprecated. Use `Vibrant.result.palettes[name]` instead")},t.prototype.getPalette=function(){var t=this,e=arguments[0],r=arguments[1],i="string"==typeof e?e:"default",n="string"==typeof e?r:e,o=new this.opts.ImageClass;return o.load(this._src).then((function(e){return t._process(e,{generators:[i]})})).then((function(e){return t._result=e,e.palettes[i]})).then((function(t){return o.remove(),n&&n(void 0,t),t})).catch((function(t){return o.remove(),n&&n(t),Promise.reject(t)}))},t.prototype.getPalettes=function(){var t=this,e=arguments[0],r=arguments[1],i=Array.isArray(e)?e:["*"],n=Array.isArray(e)?r:e,o=new this.opts.ImageClass;return o.load(this._src).then((function(e){return t._process(e,{generators:i})})).then((function(e){return t._result=e,e.palettes})).then((function(t){return o.remove(),n&&n(void 0,t),t})).catch((function(t){return o.remove(),n&&n(t),Promise.reject(t)}))},t.DefaultOpts={colorCount:64,quality:5,filters:[]},t}();e.default=s},function(t,e,r){Object.defineProperty(e,"__esModule",{value:!0}),e.applyFilters=e.ImageBase=void 0;var i=function(){function t(){}return t.prototype.scaleDown=function(t){var e=this.getWidth(),r=this.getHeight(),i=1;if(t.maxDimension>0){var n=Math.max(e,r);n>t.maxDimension&&(i=t.maxDimension/n)}else i=1/t.quality;i<1&&this.resize(e*i,r*i,i)},t}();e.ImageBase=i,e.applyFilters=function(t,e){if(e.length>0)for(var r=t.data,i=r.length/4,n=void 0,o=void 0,a=void 0,s=void 0,u=void 0,c=0;c<i;c++){o=r[0+(n=4*c)],a=r[n+1],s=r[n+2],u=r[n+3];for(var l=0;l<e.length;l++)if(!e[l](o,a,s,u)){r[n+3]=0;break}}return t}},function(t,e,r){Object.defineProperty(e,"__esModule",{value:!0}),e.Swatch=void 0;var i=r(4),n=function(){function t(t,e){this._rgb=t,this._population=e}return t.applyFilters=function(t,e){return e.length>0?t.filter((function(t){for(var r=t.r,i=t.g,n=t.b,o=0;o<e.length;o++)if(!e[o](r,i,n,255))return!1;return!0})):t},t.clone=function(e){return new t(e._rgb,e._population)},Object.defineProperty(t.prototype,"r",{get:function(){return this._rgb[0]},enumerable:!1,configurable:!0}),Object.defineProperty(t.prototype,"g",{get:function(){return this._rgb[1]},enumerable:!1,configurable:!0}),Object.defineProperty(t.prototype,"b",{get:function(){return this._rgb[2]},enumerable:!1,configurable:!0}),Object.defineProperty(t.prototype,"rgb",{get:function(){return this._rgb},enumerable:!1,configurable:!0}),Object.defineProperty(t.prototype,"hsl",{get:function(){if(!this._hsl){var t=this._rgb,e=t[0],r=t[1],n=t[2];this._hsl=i.rgbToHsl(e,r,n)}return this._hsl},enumerable:!1,configurable:!0}),Object.defineProperty(t.prototype,"hex",{get:function(){if(!this._hex){var t=this._rgb,e=t[0],r=t[1],n=t[2];this._hex=i.rgbToHex(e,r,n)}return this._hex},enumerable:!1,configurable:!0}),Object.defineProperty(t.prototype,"population",{get:function(){return this._population},enumerable:!1,configurable:!0}),t.prototype.toJSON=function(){return{rgb:this.rgb,population:this.population}},t.prototype.getRgb=function(){return this._rgb},t.prototype.getHsl=function(){return this.hsl},t.prototype.getPopulation=function(){return this._population},t.prototype.getHex=function(){return this.hex},t.prototype.getYiq=function(){if(!this._yiq){var t=this._rgb;this._yiq=(299*t[0]+587*t[1]+114*t[2])/1e3}return this._yiq},Object.defineProperty(t.prototype,"titleTextColor",{get:function(){return this._titleTextColor&&(this._titleTextColor=this.getYiq()<200?"#fff":"#000"),this._titleTextColor},enumerable:!1,configurable:!0}),Object.defineProperty(t.prototype,"bodyTextColor",{get:function(){return this._bodyTextColor&&(this._bodyTextColor=this.getYiq()<150?"#fff":"#000"),this._bodyTextColor},enumerable:!1,configurable:!0}),t.prototype.getTitleTextColor=function(){return this.titleTextColor},t.prototype.getBodyTextColor=function(){return this.bodyTextColor},t}();e.Swatch=n},function(t,e,r){function i(t){var e=/^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(t);if(!e)throw new RangeError("'"+t+"' is not a valid hex color");return[e[1],e[2],e[3]].map((function(t){return parseInt(t,16)}))}function n(t,e,r){return e/=255,r/=255,t=(t/=255)>.04045?Math.pow((t+.005)/1.055,2.4):t/12.92,e=e>.04045?Math.pow((e+.005)/1.055,2.4):e/12.92,r=r>.04045?Math.pow((r+.005)/1.055,2.4):r/12.92,[.4124*(t*=100)+.3576*(e*=100)+.1805*(r*=100),.2126*t+.7152*e+.0722*r,.0193*t+.1192*e+.9505*r]}function o(t,e,r){return e/=100,r/=108.883,t=(t/=95.047)>.008856?Math.pow(t,1/3):7.787*t+16/116,[116*(e=e>.008856?Math.pow(e,1/3):7.787*e+16/116)-16,500*(t-e),200*(e-(r=r>.008856?Math.pow(r,1/3):7.787*r+16/116))]}function a(t,e,r){var i=n(t,e,r);return o(i[0],i[1],i[2])}function s(t,e){var r=t[0],i=t[1],n=t[2],o=e[0],a=e[1],s=e[2],u=r-o,c=i-a,l=n-s,h=Math.sqrt(i*i+n*n),d=o-r,f=Math.sqrt(a*a+s*s)-h,p=Math.sqrt(u*u+c*c+l*l),g=Math.sqrt(p)>Math.sqrt(Math.abs(d))+Math.sqrt(Math.abs(f))?Math.sqrt(p*p-d*d-f*f):0;return d/=1,f/=1*(1+.045*h),g/=1*(1+.015*h),Math.sqrt(d*d+f*f+g*g)}function u(t,e){return s(a.apply(void 0,t),a.apply(void 0,e))}Object.defineProperty(e,"__esModule",{value:!0}),e.getColorDiffStatus=e.hexDiff=e.rgbDiff=e.deltaE94=e.rgbToCIELab=e.xyzToCIELab=e.rgbToXyz=e.hslToRgb=e.rgbToHsl=e.rgbToHex=e.hexToRgb=e.DELTAE94_DIFF_STATUS=void 0,e.DELTAE94_DIFF_STATUS={NA:0,PERFECT:1,CLOSE:2,GOOD:10,SIMILAR:50},e.hexToRgb=i,e.rgbToHex=function(t,e,r){return"#"+((1<<24)+(t<<16)+(e<<8)+r).toString(16).slice(1,7)},e.rgbToHsl=function(t,e,r){t/=255,e/=255,r/=255;var i=Math.max(t,e,r),n=Math.min(t,e,r),o=0,a=0,s=(i+n)/2;if(i!==n){var u=i-n;switch(a=s>.5?u/(2-i-n):u/(i+n),i){case t:o=(e-r)/u+(e<r?6:0);break;case e:o=(r-t)/u+2;break;case r:o=(t-e)/u+4}o/=6}return[o,a,s]},e.hslToRgb=function(t,e,r){var i,n,o;function a(t,e,r){return r<0&&(r+=1),r>1&&(r-=1),r<1/6?t+6*(e-t)*r:r<.5?e:r<2/3?t+(e-t)*(2/3-r)*6:t}if(0===e)i=n=o=r;else{var s=r<.5?r*(1+e):r+e-r*e,u=2*r-s;i=a(u,s,t+1/3),n=a(u,s,t),o=a(u,s,t-1/3)}return[255*i,255*n,255*o]},e.rgbToXyz=n,e.xyzToCIELab=o,e.rgbToCIELab=a,e.deltaE94=s,e.rgbDiff=u,e.hexDiff=function(t,e){return u(i(t),i(e))},e.getColorDiffStatus=function(t){return t<e.DELTAE94_DIFF_STATUS.NA?"N/A":t<=e.DELTAE94_DIFF_STATUS.PERFECT?"Perfect":t<=e.DELTAE94_DIFF_STATUS.CLOSE?"Close":t<=e.DELTAE94_DIFF_STATUS.GOOD?"Good":t<e.DELTAE94_DIFF_STATUS.SIMILAR?"Similar":"Wrong"}},function(t,e,r){var i=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}},n=i(r(6)),o=i(r(9));n.default.DefaultOpts.ImageClass=o.default,t.exports=n.default},function(t,e,r){var i=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}};Object.defineProperty(e,"__esModule",{value:!0});var n=i(r(1));n.default.DefaultOpts.quantizer="mmcq",n.default.DefaultOpts.generators=["default"],n.default.DefaultOpts.filters=["default"],e.default=n.default},function(t,e,r){Object.defineProperty(e,"__esModule",{value:!0}),e.buildProcessOptions=void 0;var i=r(0);e.buildProcessOptions=function(t,e){var r=t.colorCount,n=t.quantizer,o=t.generators,a=t.filters,s={colorCount:r},u="string"==typeof n?{name:n,options:{}}:n;return u.options=i.assignDeep({},s,u.options),i.assignDeep({},{quantizer:u,generators:o,filters:a},e)}},function(t,e,r){var i=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}};Object.defineProperty(e,"__esModule",{value:!0});var n=i(r(1)),o=r(0),a=function(){function t(t,e){void 0===e&&(e={}),this._src=t,this._opts=o.assignDeep({},n.default.DefaultOpts,e)}return t.prototype.maxColorCount=function(t){return this._opts.colorCount=t,this},t.prototype.maxDimension=function(t){return this._opts.maxDimension=t,this},t.prototype.addFilter=function(t){return this._opts.filters?this._opts.filters.push(t):this._opts.filters=[t],this},t.prototype.removeFilter=function(t){if(this._opts.filters){var e=this._opts.filters.indexOf(t);e>0&&this._opts.filters.splice(e)}return this},t.prototype.clearFilters=function(){return this._opts.filters=[],this},t.prototype.quality=function(t){return this._opts.quality=t,this},t.prototype.useImageClass=function(t){return this._opts.ImageClass=t,this},t.prototype.useGenerator=function(t,e){return this._opts.generators||(this._opts.generators=[]),this._opts.generators.push(e?{name:t,options:e}:t),this},t.prototype.useQuantizer=function(t,e){return this._opts.quantizer=e?{name:t,options:e}:t,this},t.prototype.build=function(){return new n.default(this._src,this._opts)},t.prototype.getPalette=function(t){return this.build().getPalette(t)},t.prototype.getSwatches=function(t){return this.build().getPalette(t)},t}();e.default=a},function(t,e,r){var i,n=this&&this.__extends||(i=function(t,e){return i=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(t,e){t.__proto__=e}||function(t,e){for(var r in e)e.hasOwnProperty(r)&&(t[r]=e[r])},i(t,e)},function(t,e){function r(){this.constructor=t}i(t,e),t.prototype=null===e?Object.create(e):(r.prototype=e.prototype,new r)});Object.defineProperty(e,"__esModule",{value:!0});var o=function(t){function e(){return null!==t&&t.apply(this,arguments)||this}return n(e,t),e.prototype._initCanvas=function(){var t=this.image,e=this._canvas=document.createElement("canvas"),r=e.getContext("2d");if(!r)throw new ReferenceError("Failed to create canvas context");this._context=r,e.className="@vibrant/canvas",e.style.display="none",this._width=e.width=t.width,this._height=e.height=t.height,r.drawImage(t,0,0),document.body.appendChild(e)},e.prototype.load=function(t){var e,r,i,n,o,a,s,u=this;if("string"==typeof t)e=document.createElement("img"),r=t,(s=new URL(r,location.href)).protocol===location.protocol&&s.host===location.host&&s.port===location.port||(i=window.location.href,n=r,o=new URL(i),a=new URL(n),o.protocol===a.protocol&&o.hostname===a.hostname&&o.port===a.port)||(e.crossOrigin="anonymous"),e.src=r;else{if(!(t instanceof HTMLImageElement))return Promise.reject(new Error("Cannot load buffer as an image in browser"));e=t,r=t.src}return this.image=e,new Promise((function(t,i){var n=function(){u._initCanvas(),t(u)};e.complete?n():(e.onload=n,e.onerror=function(t){return i(new Error("Fail to load image: "+r))})}))},e.prototype.clear=function(){this._context.clearRect(0,0,this._width,this._height)},e.prototype.update=function(t){this._context.putImageData(t,0,0)},e.prototype.getWidth=function(){return this._width},e.prototype.getHeight=function(){return this._height},e.prototype.resize=function(t,e,r){var i=this,n=i._canvas,o=i._context,a=i.image;this._width=n.width=t,this._height=n.height=e,o.scale(r,r),o.drawImage(a,0,0)},e.prototype.getPixelCount=function(){return this._width*this._height},e.prototype.getImageData=function(){return this._context.getImageData(0,0,this._width,this._height)},e.prototype.remove=function(){this._canvas&&this._canvas.parentNode&&this._canvas.parentNode.removeChild(this._canvas)},e}(r(2).ImageBase);e.default=o},function(t,e,r){var i=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}},n=r(5),o=i(r(11));n.use(o.default),t.exports=n},function(t,e,r){var i=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}};Object.defineProperty(e,"__esModule",{value:!0});var n=i(r(12)),o=i(r(16)),a=(new(r(17).BasicPipeline)).filter.register("default",(function(t,e,r,i){return i>=125&&!(t>250&&e>250&&r>250)})).quantizer.register("mmcq",n.default).generator.register("default",o.default);e.default=a},function(t,e,r){var i=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}};Object.defineProperty(e,"__esModule",{value:!0});var n=r(3),o=i(r(13)),a=i(r(15));function s(t,e){for(var r=t.size();t.size()<e;){var i=t.pop();if(!(i&&i.count()>0))break;var n=i.split(),o=n[0],a=n[1];if(t.push(o),a&&a.count()>0&&t.push(a),t.size()===r)break;r=t.size()}}e.default=function(t,e){if(0===t.length||e.colorCount<2||e.colorCount>256)throw new Error("Wrong MMCQ parameters");var r=o.default.build(t);r.histogram.colorCount;var i=new a.default((function(t,e){return t.count()-e.count()}));i.push(r),s(i,.75*e.colorCount);var u=new a.default((function(t,e){return t.count()*t.volume()-e.count()*e.volume()}));return u.contents=i.contents,s(u,e.colorCount-u.size()),function(t){for(var e=[];t.size();){var r=t.pop(),i=r.avg();i[0],i[1],i[2],e.push(new n.Swatch(i,r.count()))}return e}(u)}},function(t,e,r){var i=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}};Object.defineProperty(e,"__esModule",{value:!0});var n=i(r(14)),o=function(){function t(t,e,r,i,n,o,a){this.histogram=a,this._volume=-1,this._count=-1,this.dimension={r1:t,r2:e,g1:r,g2:i,b1:n,b2:o}}return t.build=function(e){var r=new n.default(e,{sigBits:5});return new t(r.rmin,r.rmax,r.gmin,r.gmax,r.bmin,r.bmax,r)},t.prototype.invalidate=function(){this._volume=this._count=-1,this._avg=null},t.prototype.volume=function(){if(this._volume<0){var t=this.dimension,e=t.r1,r=t.r2,i=t.g1,n=t.g2,o=t.b1,a=t.b2;this._volume=(r-e+1)*(n-i+1)*(a-o+1)}return this._volume},t.prototype.count=function(){if(this._count<0){for(var t=this.histogram,e=t.hist,r=t.getColorIndex,i=this.dimension,n=i.r1,o=i.r2,a=i.g1,s=i.g2,u=i.b1,c=i.b2,l=0,h=n;h<=o;h++)for(var d=a;d<=s;d++)for(var f=u;f<=c;f++)l+=e[r(h,d,f)];this._count=l}return this._count},t.prototype.clone=function(){var e=this.histogram,r=this.dimension;return new t(r.r1,r.r2,r.g1,r.g2,r.b1,r.b2,e)},t.prototype.avg=function(){if(!this._avg){var t=this.histogram,e=t.hist,r=t.getColorIndex,i=this.dimension,n=i.r1,o=i.r2,a=i.g1,s=i.g2,u=i.b1,c=i.b2,l=0,h=void 0,d=void 0,f=void 0;h=d=f=0;for(var p=n;p<=o;p++)for(var g=a;g<=s;g++)for(var m=u;m<=c;m++){var _=e[r(p,g,m)];l+=_,h+=_*(p+.5)*8,d+=_*(g+.5)*8,f+=_*(m+.5)*8}this._avg=l?[~~(h/l),~~(d/l),~~(f/l)]:[~~(8*(n+o+1)/2),~~(8*(a+s+1)/2),~~(8*(u+c+1)/2)]}return this._avg},t.prototype.contains=function(t){var e=t[0],r=t[1],i=t[2],n=this.dimension,o=n.r1,a=n.r2,s=n.g1,u=n.g2,c=n.b1,l=n.b2;return r>>=3,i>>=3,(e>>=3)>=o&&e<=a&&r>=s&&r<=u&&i>=c&&i<=l},t.prototype.split=function(){var t=this.histogram,e=t.hist,r=t.getColorIndex,i=this.dimension,n=i.r1,o=i.r2,a=i.g1,s=i.g2,u=i.b1,c=i.b2,l=this.count();if(!l)return[];if(1===l)return[this.clone()];var h,d,f=o-n+1,p=s-a+1,g=c-u+1,m=Math.max(f,p,g),_=null;h=d=0;var v=null;if(m===f){v="r",_=new Uint32Array(o+1);for(var b=n;b<=o;b++){h=0;for(var y=a;y<=s;y++)for(var k=u;k<=c;k++)h+=e[r(b,y,k)];d+=h,_[b]=d}}else if(m===p)for(v="g",_=new Uint32Array(s+1),y=a;y<=s;y++){for(h=0,b=n;b<=o;b++)for(k=u;k<=c;k++)h+=e[r(b,y,k)];d+=h,_[y]=d}else for(v="b",_=new Uint32Array(c+1),k=u;k<=c;k++){for(h=0,b=n;b<=o;b++)for(y=a;y<=s;y++)h+=e[r(b,y,k)];d+=h,_[k]=d}for(var w=-1,x=new Uint32Array(_.length),M=0;M<_.length;M++){var C=_[M];w<0&&C>d/2&&(w=M),x[M]=d-C}var O=this;return function(t){var e=t+"1",r=t+"2",i=O.dimension[e],n=O.dimension[r],o=O.clone(),a=O.clone(),s=w-i,u=n-w;for(s<=u?(n=Math.min(n-1,~~(w+u/2)),n=Math.max(0,n)):(n=Math.max(i,~~(w-1-s/2)),n=Math.min(O.dimension[r],n));!_[n];)n++;for(var c=x[n];!c&&_[n-1];)c=x[--n];return o.dimension[r]=n,a.dimension[e]=n+1,[o,a]}(v)},t}();e.default=o},function(t,e,r){Object.defineProperty(e,"__esModule",{value:!0});var i=function(){function t(t,e){this.pixels=t,this.opts=e;var r=e.sigBits,i=function(t,e,i){return(t<<2*r)+(e<<r)+i};this.getColorIndex=i;var n,o,a,s,u,c,l,h,d,f=8-r,p=new Uint32Array(1<<3*r);n=a=u=0,o=s=c=Number.MAX_VALUE;for(var g=t.length/4,m=0;m<g;){var _=4*m;m++,l=t[_+0],h=t[_+1],d=t[_+2],0!==t[_+3]&&(p[i(l>>=f,h>>=f,d>>=f)]+=1,l>n&&(n=l),l<o&&(o=l),h>a&&(a=h),h<s&&(s=h),d>u&&(u=d),d<c&&(c=d))}this._colorCount=p.reduce((function(t,e){return e>0?t+1:t}),0),this.hist=p,this.rmax=n,this.rmin=o,this.gmax=a,this.gmin=s,this.bmax=u,this.bmin=c}return Object.defineProperty(t.prototype,"colorCount",{get:function(){return this._colorCount},enumerable:!1,configurable:!0}),t}();e.default=i},function(t,e,r){Object.defineProperty(e,"__esModule",{value:!0});var i=function(){function t(t){this._comparator=t,this.contents=[],this._sorted=!1}return t.prototype._sort=function(){this._sorted||(this.contents.sort(this._comparator),this._sorted=!0)},t.prototype.push=function(t){this.contents.push(t),this._sorted=!1},t.prototype.peek=function(t){return this._sort(),t="number"==typeof t?t:this.contents.length-1,this.contents[t]},t.prototype.pop=function(){return this._sort(),this.contents.pop()},t.prototype.size=function(){return this.contents.length},t.prototype.map=function(t){return this._sort(),this.contents.map(t)},t}();e.default=i},function(t,e,r){Object.defineProperty(e,"__esModule",{value:!0});var i=r(3),n=r(4),o={targetDarkLuma:.26,maxDarkLuma:.45,minLightLuma:.55,targetLightLuma:.74,minNormalLuma:.3,targetNormalLuma:.5,maxNormalLuma:.7,targetMutesSaturation:.3,maxMutesSaturation:.4,targetVibrantSaturation:1,minVibrantSaturation:.35,weightSaturation:3,weightLuma:6.5,weightPopulation:.5};function a(t,e,r,i,n,o,a,s,u,c){var l=null,h=0;return e.forEach((function(e){var d=e.hsl,f=d[1],p=d[2];if(f>=s&&f<=u&&p>=n&&p<=o&&!function(t,e){return t.Vibrant===e||t.DarkVibrant===e||t.LightVibrant===e||t.Muted===e||t.DarkMuted===e||t.LightMuted===e}(t,e)){var g=function(t,e,r,i,n,o,a){function s(t,e){return 1-Math.abs(t-e)}return function(){for(var t=[],e=0;e<arguments.length;e++)t[e]=arguments[e];for(var r=0,i=0,n=0;n<t.length;n+=2){var o=t[n],a=t[n+1];r+=o*a,i+=a}return r/i}(s(t,e),a.weightSaturation,s(r,i),a.weightLuma,n/o,a.weightPopulation)}(f,a,p,i,e.population,r,c);(null===l||g>h)&&(l=e,h=g)}})),l}e.default=function(t,e){e=Object.assign({},o,e);var r=function(t){var e=0;return t.forEach((function(t){e=Math.max(e,t.population)})),e}(t),s=function(t,e,r){var i={Vibrant:null,DarkVibrant:null,LightVibrant:null,Muted:null,DarkMuted:null,LightMuted:null};return i.Vibrant=a(i,t,e,r.targetNormalLuma,r.minNormalLuma,r.maxNormalLuma,r.targetVibrantSaturation,r.minVibrantSaturation,1,r),i.LightVibrant=a(i,t,e,r.targetLightLuma,r.minLightLuma,1,r.targetVibrantSaturation,r.minVibrantSaturation,1,r),i.DarkVibrant=a(i,t,e,r.targetDarkLuma,0,r.maxDarkLuma,r.targetVibrantSaturation,r.minVibrantSaturation,1,r),i.Muted=a(i,t,e,r.targetNormalLuma,r.minNormalLuma,r.maxNormalLuma,r.targetMutesSaturation,0,r.maxMutesSaturation,r),i.LightMuted=a(i,t,e,r.targetLightLuma,r.minLightLuma,1,r.targetMutesSaturation,0,r.maxMutesSaturation,r),i.DarkMuted=a(i,t,e,r.targetDarkLuma,0,r.maxDarkLuma,r.targetMutesSaturation,0,r.maxMutesSaturation,r),i}(t,r,e);return function(t,e,r){if(!t.Vibrant&&!t.DarkVibrant&&!t.LightVibrant){if(!t.DarkVibrant&&t.DarkMuted){var o=t.DarkMuted.hsl,a=o[0],s=o[1],u=o[2];u=r.targetDarkLuma,t.DarkVibrant=new i.Swatch(n.hslToRgb(a,s,u),0)}if(!t.LightVibrant&&t.LightMuted){var c=t.LightMuted.hsl;a=c[0],s=c[1],u=c[2],u=r.targetDarkLuma,t.DarkVibrant=new i.Swatch(n.hslToRgb(a,s,u),0)}}if(!t.Vibrant&&t.DarkVibrant){var l=t.DarkVibrant.hsl;a=l[0],s=l[1],u=l[2],u=r.targetNormalLuma,t.Vibrant=new i.Swatch(n.hslToRgb(a,s,u),0)}else if(!t.Vibrant&&t.LightVibrant){var h=t.LightVibrant.hsl;a=h[0],s=h[1],u=h[2],u=r.targetNormalLuma,t.Vibrant=new i.Swatch(n.hslToRgb(a,s,u),0)}if(!t.DarkVibrant&&t.Vibrant){var d=t.Vibrant.hsl;a=d[0],s=d[1],u=d[2],u=r.targetDarkLuma,t.DarkVibrant=new i.Swatch(n.hslToRgb(a,s,u),0)}if(!t.LightVibrant&&t.Vibrant){var f=t.Vibrant.hsl;a=f[0],s=f[1],u=f[2],u=r.targetLightLuma,t.LightVibrant=new i.Swatch(n.hslToRgb(a,s,u),0)}if(!t.Muted&&t.Vibrant){var p=t.Vibrant.hsl;a=p[0],s=p[1],u=p[2],u=r.targetMutesSaturation,t.Muted=new i.Swatch(n.hslToRgb(a,s,u),0)}if(!t.DarkMuted&&t.DarkVibrant){var g=t.DarkVibrant.hsl;a=g[0],s=g[1],u=g[2],u=r.targetMutesSaturation,t.DarkMuted=new i.Swatch(n.hslToRgb(a,s,u),0)}if(!t.LightMuted&&t.LightVibrant){var m=t.LightVibrant.hsl;a=m[0],s=m[1],u=m[2],u=r.targetMutesSaturation,t.LightMuted=new i.Swatch(n.hslToRgb(a,s,u),0)}}(s,0,e),s}},function(t,e,r){var i=this&&this.__awaiter||function(t,e,r,i){return new(r||(r=Promise))((function(n,o){function a(t){try{u(i.next(t))}catch(t){o(t)}}function s(t){try{u(i.throw(t))}catch(t){o(t)}}function u(t){var e;t.done?n(t.value):(e=t.value,e instanceof r?e:new r((function(t){t(e)}))).then(a,s)}u((i=i.apply(t,e||[])).next())}))},n=this&&this.__generator||function(t,e){var r,i,n,o,a={label:0,sent:function(){if(1&n[0])throw n[1];return n[1]},trys:[],ops:[]};return o={next:s(0),throw:s(1),return:s(2)},"function"==typeof Symbol&&(o[Symbol.iterator]=function(){return this}),o;function s(o){return function(s){return function(o){if(r)throw new TypeError("Generator is already executing.");for(;a;)try{if(r=1,i&&(n=2&o[0]?i.return:o[0]?i.throw||((n=i.return)&&n.call(i),0):i.next)&&!(n=n.call(i,o[1])).done)return n;switch(i=0,n&&(o=[2&o[0],n.value]),o[0]){case 0:case 1:n=o;break;case 4:return a.label++,{value:o[1],done:!1};case 5:a.label++,i=o[1],o=[0];continue;case 7:o=a.ops.pop(),a.trys.pop();continue;default:if(!((n=(n=a.trys).length>0&&n[n.length-1])||6!==o[0]&&2!==o[0])){a=0;continue}if(3===o[0]&&(!n||o[1]>n[0]&&o[1]<n[3])){a.label=o[1];break}if(6===o[0]&&a.label<n[1]){a.label=n[1],n=o;break}if(n&&a.label<n[2]){a.label=n[2],a.ops.push(o);break}n[2]&&a.ops.pop(),a.trys.pop();continue}o=e.call(t,a)}catch(t){o=[6,t],i=0}finally{r=n=0}if(5&o[0])throw o[1];return{value:o[0]?o[1]:void 0,done:!0}}([o,s])}}};Object.defineProperty(e,"__esModule",{value:!0}),e.BasicPipeline=e.Stage=void 0;var o=r(2),a=function(){function t(t){this.pipeline=t,this._map={}}return t.prototype.names=function(){return Object.keys(this._map)},t.prototype.has=function(t){return!!this._map[t]},t.prototype.get=function(t){return this._map[t]},t.prototype.register=function(t,e){return this._map[t]=e,this.pipeline},t}();e.Stage=a;var s=function(){function t(){this.filter=new a(this),this.quantizer=new a(this),this.generator=new a(this)}return t.prototype._buildProcessTasks=function(t){var e=this,r=t.filters,i=t.quantizer,n=t.generators;return 1===n.length&&"*"===n[0]&&(n=this.generator.names()),{filters:r.map((function(t){return o(e.filter,t)})),quantizer:o(this.quantizer,i),generators:n.map((function(t){return o(e.generator,t)}))};function o(t,e){var r,i;return"string"==typeof e?r=e:(r=e.name,i=e.options),{name:r,fn:t.get(r),options:i}}},t.prototype.process=function(t,e){return i(this,void 0,void 0,(function(){var r,i,o,a,s,u,c;return n(this,(function(n){switch(n.label){case 0:return r=this._buildProcessTasks(e),i=r.filters,o=r.quantizer,a=r.generators,[4,this._filterColors(i,t)];case 1:return s=n.sent(),[4,this._generateColors(o,s)];case 2:return u=n.sent(),[4,this._generatePalettes(a,u)];case 3:return c=n.sent(),[2,{colors:u,palettes:c}]}}))}))},t.prototype._filterColors=function(t,e){return Promise.resolve(o.applyFilters(e,t.map((function(t){return t.fn}))))},t.prototype._generateColors=function(t,e){return Promise.resolve(t.fn(e.data,t.options))},t.prototype._generatePalettes=function(t,e){return i(this,void 0,void 0,(function(){var r;return n(this,(function(i){switch(i.label){case 0:return[4,Promise.all(t.map((function(t){var r=t.fn,i=t.options;return Promise.resolve(r(e,i))})))];case 1:return r=i.sent(),[2,Promise.resolve(r.reduce((function(e,r,i){return e[t[i].name]=r,e}),{}))]}}))}))},t}();e.BasicPipeline=s}])},t.exports=r()})),E=v(V);E._pipeline.generator.register("default",(e=>{e.sort(((t,e)=>e.population-t.population));const r=e[0];let i;const n=new Map,o=(e,i)=>(n.has(e)||n.set(e,t(r.rgb,i)),n.get(e)>4.5);for(let t=1;t<e.length&&void 0===i;t++){if(o(e[t].hex,e[t].rgb)){false,i=e[t].rgb;break}const r=e[t];false;for(let n=t+1;n<e.length;n++){const t=e[n],a=Math.abs(r.rgb[0]-t.rgb[0])+Math.abs(r.rgb[1]-t.rgb[1])+Math.abs(r.rgb[2]-t.rgb[2]);if(!(a>150)&&o(t.hex,t.rgb)){false,i=t.rgb;break}}}return void 0===i&&(i=r.getYiq()<200?[255,255,255]:[0,0,0]),{foreground:new r.constructor(i,0),background:r}}));e([u("hui-marquee")],(function(t,e){class r extends e{constructor(...e){super(...e),t(this)}}return{F:r,d:[{kind:"field",decorators:[i()],key:"text",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"active",value:void 0},{kind:"field",decorators:[i({reflect:!0,type:Boolean,attribute:"animating"})],key:"_animating",value:()=>!1},{kind:"method",key:"firstUpdated",value:function(t){n(o(r.prototype),"firstUpdated",this).call(this,t),this.addEventListener("mouseover",(()=>this.classList.add("hovering")),{capture:!0}),this.addEventListener("mouseout",(()=>this.classList.remove("hovering")))}},{kind:"method",key:"updated",value:function(t){n(o(r.prototype),"updated",this).call(this,t),t.has("text")&&this._animating&&(this._animating=!1),t.has("active")&&this.active&&this.offsetWidth<this.scrollWidth&&(this._animating=!0)}},{kind:"method",key:"render",value:function(){return this.text?a`
      <div class="marquee-inner" @animationiteration=${this._onIteration}>
        <span>${this.text}</span>
        ${this._animating?a` <span>${this.text}</span> `:""}
      </div>
    `:a``}},{kind:"method",key:"_onIteration",value:function(){this.active||(this._animating=!1)}},{kind:"get",static:!0,key:"styles",value:function(){return s`
      :host {
        display: flex;
        position: relative;
        align-items: center;
        height: 1.2em;
        contain: strict;
      }

      .marquee-inner {
        position: absolute;
        left: 0;
        right: 0;
        text-overflow: ellipsis;
        overflow: hidden;
      }

      :host(.hovering) .marquee-inner {
        text-overflow: initial;
        overflow: initial;
      }

      :host([animating]) .marquee-inner {
        left: initial;
        right: initial;
        animation: marquee 10s linear infinite;
      }

      :host([animating]) .marquee-inner span {
        padding-right: 16px;
      }

      @keyframes marquee {
        0% {
          transform: translateX(0%);
        }
        100% {
          transform: translateX(-50%);
        }
      }
    `}}]}}),r);let $=e([u("hui-media-control-card")],(function(t,e){class r extends e{constructor(...e){super(...e),t(this)}}return{F:r,d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await import("./c.ac85cb69.js"),document.createElement("hui-media-control-card-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(t,e,r){return{type:"media-control",entity:x(t,1,e,r,["media_player"])[0]||""}}},{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[c()],key:"_config",value:void 0},{kind:"field",decorators:[c()],key:"_foregroundColor",value:void 0},{kind:"field",decorators:[c()],key:"_backgroundColor",value:void 0},{kind:"field",decorators:[c()],key:"_narrow",value:()=>!1},{kind:"field",decorators:[c()],key:"_veryNarrow",value:()=>!1},{kind:"field",decorators:[c()],key:"_cardHeight",value:()=>0},{kind:"field",decorators:[l("mwc-linear-progress")],key:"_progressBar",value:void 0},{kind:"field",decorators:[c()],key:"_marqueeActive",value:()=>!1},{kind:"field",key:"_progressInterval",value:void 0},{kind:"field",key:"_resizeObserver",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(t){if(!t.entity||"media_player"!==t.entity.split(".")[0])throw new Error("Specify an entity from within the media_player domain");this._config=t}},{kind:"method",key:"connectedCallback",value:function(){if(n(o(r.prototype),"connectedCallback",this).call(this),this.updateComplete.then((()=>this._attachObserver())),!this.hass||!this._config)return;const t=this._stateObj;t&&!this._progressInterval&&this._showProgressBar&&"playing"===t.state&&(this._progressInterval=window.setInterval((()=>this._updateProgressBar()),1e3))}},{kind:"method",key:"disconnectedCallback",value:function(){this._progressInterval&&(clearInterval(this._progressInterval),this._progressInterval=void 0),this._resizeObserver&&this._resizeObserver.disconnect()}},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return a``;const t=this._stateObj;if(!t)return a`
        <hui-warning>
          ${M(this.hass,this._config.entity)}
        </hui-warning>
      `;const e={"background-image":this._image?`url(${this.hass.hassUrl(this._image)})`:"none",width:`${this._cardHeight}px`,"background-color":this._backgroundColor||""},r={"background-image":`linear-gradient(to right, ${this._backgroundColor}, ${this._backgroundColor+"00"})`,width:`${this._cardHeight}px`},i=t.state,n="off"===i,o=b.includes(i)||"off"===i&&!y(t,C),s=!this._image,u=O(t,!1),c=u&&(!this._veryNarrow||n||"idle"===i||"on"===i),l=D(t),g=L(t.attributes.media_title);return a`
      <ha-card>
        <div
          class="background ${h({"no-image":s,off:n||o,unavailable:o})}"
        >
          <div
            class="color-block"
            style=${d({"background-color":this._backgroundColor||""})}
          ></div>
          <div
            class="no-img"
            style=${d({"background-color":this._backgroundColor||""})}
          ></div>
          <div class="image" style=${d(e)}></div>
          ${s?"":a`
                <div
                  class="color-gradient"
                  style=${d(r)}
                ></div>
              `}
        </div>
        <div
          class="player ${h({"no-image":s,narrow:this._narrow&&!this._veryNarrow,off:n||o,"no-progress":this._veryNarrow||!this._showProgressBar,"no-controls":!c})}"
          style=${d({color:this._foregroundColor||""})}
        >
          <div class="top-info">
            <div class="icon-name">
              <ha-state-icon class="icon" .state=${t}></ha-state-icon>
              <div>
                ${this._config.name||k(this.hass.states[this._config.entity])}
              </div>
            </div>
            <div>
              <ha-icon-button
                .path=${f}
                .label=${this.hass.localize("ui.panel.lovelace.cards.show_more_info")}
                class="more-info"
                @click=${this._handleMoreInfo}
              ></ha-icon-button>
            </div>
          </div>
          ${!o&&(l||g||c)?a`
                <div>
                  <div class="title-controls">
                    ${l||g?a`
                          <div class="media-info">
                            <hui-marquee
                              .text=${g||l}
                              .active=${this._marqueeActive}
                              @mouseover=${this._marqueeMouseOver}
                              @mouseleave=${this._marqueeMouseLeave}
                            ></hui-marquee>
                            ${g?l:""}
                          </div>
                        `:""}
                    ${c?a`
                          <div class="controls">
                            ${u.map((t=>a`
                                <ha-icon-button
                                  .label=${this.hass.localize(`ui.card.media_player.${t.action}`)}
                                  .path=${t.icon}
                                  action=${t.action}
                                  @click=${this._handleClick}
                                >
                                </ha-icon-button>
                              `))}
                            ${y(t,P)?a`
                                  <ha-icon-button
                                    class="browse-media"
                                    .label=${this.hass.localize("ui.card.media_player.browse_media")}
                                    .path=${p}
                                    @click=${this._handleBrowseMedia}
                                  ></ha-icon-button>
                                `:""}
                          </div>
                        `:""}
                  </div>
                  ${this._showProgressBar?a`
                        <mwc-linear-progress
                          determinate
                          style=${d({"--mdc-theme-primary":this._foregroundColor||"var(--accent-color)",cursor:y(t,S)?"pointer":"initial"})}
                          @click=${this._handleSeek}
                        >
                        </mwc-linear-progress>
                      `:""}
                </div>
              `:""}
        </div>
      </ha-card>
    `}},{kind:"method",key:"shouldUpdate",value:function(t){return T(this,t)}},{kind:"method",key:"firstUpdated",value:function(){this._attachObserver()}},{kind:"method",key:"willUpdate",value:function(t){var e,i;if(n(o(r.prototype),"willUpdate",this).call(this,t),this.hasUpdated||this._measureCard(),!this._config||!this.hass||!t.has("_config")&&!t.has("hass"))return;if(!this._stateObj)return this._progressInterval&&(clearInterval(this._progressInterval),this._progressInterval=void 0),this._foregroundColor=void 0,void(this._backgroundColor=void 0);const a=t.get("hass"),s=(null==a||null===(e=a.states[this._config.entity])||void 0===e?void 0:e.attributes.entity_picture_local)||(null==a||null===(i=a.states[this._config.entity])||void 0===i?void 0:i.attributes.entity_picture);if(!this._image)return this._foregroundColor=void 0,void(this._backgroundColor=void 0);this._image!==s&&this._setColors()}},{kind:"method",key:"updated",value:function(t){if(!this._config||!this.hass||!this._stateObj||!t.has("_config")&&!t.has("hass"))return;const e=this._stateObj,r=t.get("hass"),i=t.get("_config");r&&i&&r.themes===this.hass.themes&&i.theme===this._config.theme||g(this,this.hass.themes,this._config.theme),this._updateProgressBar(),!this._progressInterval&&this._showProgressBar&&"playing"===e.state?this._progressInterval=window.setInterval((()=>this._updateProgressBar()),1e3):!this._progressInterval||this._showProgressBar&&"playing"===e.state||(clearInterval(this._progressInterval),this._progressInterval=void 0)}},{kind:"get",key:"_image",value:function(){if(!this.hass||!this._config)return;const t=this._stateObj;return t?t.attributes.entity_picture_local||t.attributes.entity_picture:void 0}},{kind:"get",key:"_showProgressBar",value:function(){if(!this.hass||!this._config||this._narrow)return!1;const t=this._stateObj;return!!t&&(("playing"===t.state||"paused"===t.state)&&"media_duration"in t.attributes&&"media_position"in t.attributes)}},{kind:"method",key:"_measureCard",value:function(){const t=this.shadowRoot.querySelector("ha-card");t&&(this._narrow=t.offsetWidth<350,this._veryNarrow=t.offsetWidth<300,this._cardHeight=t.offsetHeight)}},{kind:"method",key:"_attachObserver",value:async function(){this._resizeObserver||(await j(),this._resizeObserver=new ResizeObserver(w((()=>this._measureCard()),250,!1)));const t=this.shadowRoot.querySelector("ha-card");t&&this._resizeObserver.observe(t)}},{kind:"method",key:"_handleMoreInfo",value:function(){m(this,"hass-more-info",{entityId:this._config.entity})}},{kind:"method",key:"_handleBrowseMedia",value:function(){z(this,{action:"play",entityId:this._config.entity,mediaPickedCallback:t=>this._playMedia(t.item.media_content_id,t.item.media_content_type)})}},{kind:"method",key:"_playMedia",value:function(t,e){this.hass.callService("media_player","play_media",{entity_id:this._config.entity,media_content_id:t,media_content_type:e})}},{kind:"method",key:"_handleClick",value:function(t){I(this.hass,this._stateObj,t.currentTarget.getAttribute("action"))}},{kind:"method",key:"_updateProgressBar",value:function(){var t;this._progressBar&&null!==(t=this._stateObj)&&void 0!==t&&t.attributes.media_duration&&(this._progressBar.progress=q(this._stateObj)/this._stateObj.attributes.media_duration)}},{kind:"get",key:"_stateObj",value:function(){return this.hass.states[this._config.entity]}},{kind:"method",key:"_handleSeek",value:function(t){const e=this._stateObj;if(!y(e,S))return;const r=this._progressBar.offsetWidth,i=t.offsetX/r,n=this._stateObj.attributes.media_duration*i;this.hass.callService("media_player","media_seek",{entity_id:this._config.entity,seek_position:n})}},{kind:"method",key:"_setColors",value:async function(){if(this._image)try{const{foreground:t,background:e}=await((t,e=16)=>new E(t,{colorCount:e}).getPalette().then((({foreground:t,background:e})=>({background:e,foreground:t}))))(this.hass.hassUrl(this._image));this._backgroundColor=e.hex,this._foregroundColor=t.hex}catch(t){console.error("Error getting Image Colors",t),this._foregroundColor=void 0,this._backgroundColor=void 0}}},{kind:"method",key:"_marqueeMouseOver",value:function(){this._marqueeActive||(this._marqueeActive=!0)}},{kind:"method",key:"_marqueeMouseLeave",value:function(){this._marqueeActive&&(this._marqueeActive=!1)}},{kind:"get",static:!0,key:"styles",value:function(){return s`
      ha-card {
        overflow: hidden;
        height: 100%;
      }

      .background {
        display: flex;
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
        transition: filter 0.8s;
      }

      .color-block {
        background-color: var(--primary-color);
        transition: background-color 0.8s;
        width: 100%;
      }

      .color-gradient {
        position: absolute;
        background-image: linear-gradient(
          to right,
          var(--primary-color),
          transparent
        );
        height: 100%;
        right: 0;
        opacity: 1;
        transition: width 0.8s, opacity 0.8s linear 0.8s;
      }

      .image {
        background-color: var(--primary-color);
        background-position: center;
        background-size: cover;
        background-repeat: no-repeat;
        position: absolute;
        right: 0;
        height: 100%;
        opacity: 1;
        transition: width 0.8s, background-image 0.8s, background-color 0.8s,
          background-size 0.8s, opacity 0.8s linear 0.8s;
      }

      .no-image .image {
        opacity: 0;
      }

      .no-img {
        background-color: var(--primary-color);
        background-size: initial;
        background-repeat: no-repeat;
        background-position: center center;
        padding-bottom: 0;
        position: absolute;
        right: 0;
        height: 100%;
        background-image: url("/static/images/card_media_player_bg.png");
        width: 50%;
        transition: opacity 0.8s, background-color 0.8s;
      }

      .off .image,
      .off .color-gradient {
        opacity: 0;
        transition: opacity 0s, width 0.8s;
        width: 0;
      }

      .unavailable .no-img,
      .background:not(.off):not(.no-image) .no-img {
        opacity: 0;
      }

      .player {
        position: relative;
        padding: 16px;
        height: 100%;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        color: var(--text-primary-color);
        transition-property: color, padding;
        transition-duration: 0.4s;
      }

      .controls {
        padding: 8px 8px 8px 0;
        display: flex;
        justify-content: flex-start;
        align-items: center;
        transition: padding, color;
        transition-duration: 0.4s;
        margin-left: -12px;
      }

      .controls > div {
        display: flex;
        align-items: center;
      }

      .controls ha-icon-button {
        --mdc-icon-button-size: 44px;
        --mdc-icon-size: 30px;
      }

      ha-icon-button[action="media_play"],
      ha-icon-button[action="media_play_pause"],
      ha-icon-button[action="media_pause"],
      ha-icon-button[action="media_stop"],
      ha-icon-button[action="turn_on"],
      ha-icon-button[action="turn_off"] {
        --mdc-icon-button-size: 56px;
        --mdc-icon-size: 40px;
      }

      ha-icon-button.browse-media {
        position: absolute;
        right: 4px;
        --mdc-icon-size: 24px;
      }

      .top-info {
        display: flex;
        justify-content: space-between;
      }

      .icon-name {
        display: flex;
        height: fit-content;
        align-items: center;
      }

      .icon-name ha-state-icon {
        padding-right: 8px;
      }

      .more-info {
        position: absolute;
        top: 4px;
        right: 4px;
      }

      .media-info {
        text-overflow: ellipsis;
        white-space: nowrap;
        overflow: hidden;
      }

      hui-marquee {
        font-size: 1.2em;
        margin: 0px 0 4px;
      }

      .title-controls {
        padding-top: 16px;
      }

      mwc-linear-progress {
        width: 100%;
        margin-top: 4px;
        --mdc-linear-progress-buffer-color: rgba(200, 200, 200, 0.5);
      }

      .no-image .controls {
        padding: 0;
      }

      .off.background {
        filter: grayscale(1);
      }

      .narrow .controls,
      .no-progress .controls {
        padding-bottom: 0;
      }

      .narrow ha-icon-button {
        --mdc-icon-button-size: 40px;
        --mdc-icon-size: 28px;
      }

      .narrow ha-icon-button[action="media_play"],
      .narrow ha-icon-button[action="media_play_pause"],
      .narrow ha-icon-button[action="media_pause"],
      .narrow ha-icon-button[action="turn_on"] {
        --mdc-icon-button-size: 50px;
        --mdc-icon-size: 36px;
      }

      .narrow ha-icon-button.browse-media {
        --mdc-icon-size: 24px;
      }

      .no-progress.player:not(.no-controls) {
        padding-bottom: 0px;
      }
    `}}]}}),r);export{$ as HuiMediaControlCard};
