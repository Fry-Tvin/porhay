/* Site form attribution, v20261124. Never synthesize advertising identifiers. */
(function (w) {
  'use strict';
  var KEY='porhay_attribution', TTL=90*86400000, memory={};
  var keys=['utm_source','utm_medium','utm_campaign','utm_content','utm_term','yclid'];
  function read(store,key){try{return store.getItem(key)||'';}catch(e){return '';}}
  function storage(name){try{return w[name];}catch(e){return null;}}
  function put(store,key,value){try{store.setItem(key,value);}catch(e){}}
  var local=storage('localStorage'), session=storage('sessionStorage');
  function get(){
    var value=memory;
    try{var saved=JSON.parse(read(local,KEY)||read(session,KEY)||'null');if(saved)value=saved;}catch(e){}
    if(value.ts && Date.now()-value.ts>=0 && Date.now()-value.ts<=TTL)return value;
    return {};
  }
  function capture(){
    var old=get(), data={}, params=new URLSearchParams(location.search), tagged=false;
    keys.forEach(function(k){var v=params.get(k);if(v){data[k]=v;tagged=true;}});
    var ref=document.referrer||'',external=false;
    try{external=!!ref && new URL(ref).origin!==location.origin;}catch(e){}
    if(!tagged && old.ts){memory=old;return;}
    if(external)data.referrer=ref;
    if(!tagged && !external){
      try{var legacy=JSON.parse(read(session,'attribution')||'{}');keys.concat(['referrer']).forEach(function(k){if(legacy[k])data[k]=legacy[k];});}catch(e){}
    }
    data.ts=Date.now();memory=data;
    put(local,KEY,JSON.stringify(data));put(session,KEY,JSON.stringify(data));
  }
  function cookieId(){var m=document.cookie.match(/(?:^|;\s*)_ym_uid=([^;]+)/);return m?m[1]:'';}
  function clientId(callback){
    var done=false;
    function finish(id){
      if(id)put(local,'porhay_cid',String(id));
      if(done)return;done=true;callback(id||cookieId()||read(local,'porhay_cid')||'');
    }
    var cookie=cookieId();if(cookie){finish(cookie);return;}
    try{if(w.ym){w.ym(112256802,'getClientID',finish);setTimeout(function(){finish('');},1500);}else finish('');}catch(e){finish('');}
  }
  capture();w.PorhayAttribution={get:get,clientId:clientId};
})(window);
