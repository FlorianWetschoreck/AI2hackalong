# AI2hackalong
This branch contains the solution to the seventh and final hackalong of AI2 2016. 

In this week, we will add a rich Web user interface to our solution, which is based on HTMl5, CSS3 and JavaScript. For this, we will use the django template mechanism, which will allow us to develop HTML templates for Web pages, that can be filled with content from the django view component. Moreover, we will use AJAX to allow the user to dynamically select whether the product page should show the most helpful or the most critical review of a product. Our solution will be based on last week's solution which uses XML and XSLT to automaticaly transform XML reviews delivered by a RESTful .NET product review service into HTML representations. 

To test the example solution of this #hackalong, you will have to follow these steps: 

1.) Right-click on the project ReviewService and click Debug -> "Start new instance" to first start the RESTful product review service. 
2.) Right-click the KITshop project and click Debug -> "Start new instance" to launch the django web server. 
3.) Now you can enter the URL of a product page in the browser, e.g. http://localhost:8000/product/123
