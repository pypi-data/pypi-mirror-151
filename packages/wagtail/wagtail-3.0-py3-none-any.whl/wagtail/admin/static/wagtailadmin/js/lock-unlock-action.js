window.LockUnlockAction=function(e,n){document.querySelectorAll("[data-action-lock-unlock]").forEach((function(t){t.addEventListener("click",(function(o){o.stopPropagation();var a=document.createElement("form");a.action=t.dataset.url,a.method="POST";var d=document.createElement("input");if(d.type="hidden",d.name="csrfmiddlewaretoken",d.value=e,a.appendChild(d),void 0!==n){var c=document.createElement("input");c.type="hidden",c.name="next",c.value=n,a.appendChild(c)}document.body.appendChild(a),a.submit()}),{capture:!0})}))};