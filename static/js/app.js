function addPhoto(){
    d3.json("/image").then(
        console.log()
        let prediction = 
        if (prediction < 700){
            document.getElementById("image").innerHTML = '<img src="https://30a.com/wp-content/uploads/2018/02/Webp.net-compress-image-11-1.jpg" width="200" height="100" alt="good">';
        }
        else if (prediction >700 && prediction<1000){
            document.getElementById("image").innerHTML = '<img src="https://cdn11.bigcommerce.com/s-5d127/images/stencil/500x659/products/564/1172/FS_Custom_Caution__33976__69789.1561495177.jpg?c=2" width="200" height="100" alt="caution">';
        }
        else if (prediction>1000){
            document.getElementById("image").innerHTML = '<img src="https://images.all-free-download.com/images/graphiclarge/no_swimming_sign_on_wite_background_6847861.jpg" width="200" height="100" alt="bad">';
        }
)}
