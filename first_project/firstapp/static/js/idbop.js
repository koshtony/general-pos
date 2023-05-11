
 //  initiate connection to  indexDB

 var dbPromise = idb.open('stocks-db', 1, function(upgradeDb) {


 upgradeDb.createObjectStore('stocks',{keyPath:'pk'});

});


// fetch data from actual database -> populate to indexDB

 var data_url = 'http://127.0.0.1:8000/feeds_indexDB'

 fetch(data_url).then(function(response){

  return response.json();

 }).then(function(data){

  console.log(data)

  dbPromise.then(function(db){

   var tx = db.transaction('stocks', 'readwrite');
     var stocksStore = tx.objectStore('stocks');

     for(var key in data){

      if (data.hasOwnProperty(key)) {

         stocksStore.put(data[key]); 
      }

     }
  });
 });


// display data 

 dbPromise.then( function(db){

 var tx = db.transaction('stocks','readonly');
 var stocksStore = tx.objectStore('stocks');
 return stocksStore.openCursor();

 }).then(function logItems(cursor){

  if (!cursor){

      return;
  }
for (var value in cursor.value){
     

         
          for(var key in cursor.value[value]) {

      
          
          $("#prodDiv").html(

`

             
                  
                  <div class="col-6 col-sm-6 col-md-3 col-lg-3 mt-2" >
                    <div class="prods">
                    <div class="card p-0 m-0">
                      <div class="card-body p-0 m-0 b-0">
                        <a onclick="counter(${cursor.value["pk"]},${cursor.value[value]["p_name"]},${cursor.value[value]["p_name"]});">
                    
                        </a>
                      </div>
                      
                      
                      
                    
                     <span id="${cursor.value[value]["p_name"]}">${cursor.value[value]["p_name"]}</span>
                      
                      <div class="card-footer cf">

                        
                        <div class="row">
                          <div class="col-6 col-sm-6 col-md-6 col-lg-6">
                            <p  id="${cursor.value[value]["p_price"]}">Ksh ${cursor.value[value]["p_name"]} </p>
                            off <input type="number" id="p${cursor.value["pk"]}" value="${cursor.value[value]["p_disc"]}" style="width:50px">
                            <br>
                            <br>
                            qty <input type="number" id="${cursor.value["pk"]}" value="1" style="width:50px; height:30px">
                          </div>
                          
                          <div class="col-6 col-sm-6 col-md-6 col-lg-6 text-right">
                            
                            <button type="button" class="btn-sm btn btn-info" id="subLink" onclick="counter(${cursor.value["pk"]},${cursor.value[value]["p_name"]},${cursor.value[value]["p_price"]});">
                              
                              <i class="fa fa-cart-plus" aria-hidden="true"></i>
                        
                            
                              
                            </button>
                            
                            
                            
                          </div>
                        </div>
                      </div>
                    </div>
                    </div>
                  </div>
                
             
               


             





`

)
     
      }
  

  }
  
});



