using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

// To include these namespaces, you will have to add reference  to the 
// System.ServiceModel and the System.ServiceModel.Web assemblies. This can be done
// by right-clicking the ReviewService project in the project explorer and then selecting 
// Add -> Reference (Hinzufügen -> Verweis)
using System.ServiceModel;
using System.ServiceModel.Web;
using System.ServiceModel.Description;

namespace ReviewService
{
   
    // This struct contains all data of a single product review
    public struct Review
    {
        public Review(string ReviewID, string ProductID, string User, string ReviewText, int Rating, int HelpfulVotes)
        {
            this.ReviewID = ReviewID;
            this.ProductID = ProductID;
            this.User = User;
            this.ReviewText = ReviewText;
            this.Rating = Rating;
            this.HelpfulVotes = HelpfulVotes;
        }

        public string ReviewID;
        public string ProductID;

        public string User;
        public string ReviewText;

        public int Rating;
        public int HelpfulVotes;
    }

    /* This is the main implementation of our Product Review service
        The special attributes before the class and method definitions tell Windows Communication Foundation 
        which of the methods should be exposed as services. For the SOAP service, the method names will be 
        used automatically. For the RESTful Web Service we can additionally use the WebGet attribute to 
        specify (i) how REST URIs map to methods of our implementation, and (ii) in what format the results 
        shall be returned.

        In our example, we will return results as JSON documents (later more)
    */

    [ServiceContract()]
    [ServiceBehavior(InstanceContextMode =InstanceContextMode.Single)]
    public class ProductReviewService
    {
        public List<Review> reviews = new List<Review>();

        [OperationContract]
        [WebGet(UriTemplate = "/products/{productID}/AvgRating", ResponseFormat = WebMessageFormat.Xml)]
        public double GetAvgRating(string productID)
        {
            return reviews.Where(r => r.ProductID == productID).Select(r => r.Rating).Average();
        }

        [OperationContract]
        [WebGet(UriTemplate = "/products/{productID}/MostHelpfulReview", ResponseFormat = WebMessageFormat.Xml)]
        public Review GetMostHelpfulReview(string productID)
        {
            Console.WriteLine("MostHelpfulReview");
            return reviews.OrderByDescending(x => x.HelpfulVotes).First();
        }

        [OperationContract]
        [WebGet(UriTemplate = "/products/{productID}/MostCriticalReview", ResponseFormat = WebMessageFormat.Xml)]
        public Review GetMostCriticalReview(string productID)
        {
            Console.WriteLine("MostCriticalReview");
            return reviews.OrderBy(x => x.Rating).First();
        }

        [OperationContract]
        [WebGet(UriTemplate = "reviews/{reviewID}", ResponseFormat = WebMessageFormat.Xml)]
        public Review GetReview(string reviewID)
        {
            return reviews.Where(r => r.ReviewID == reviewID).First();
        }

        [OperationContract]
        [WebGet(UriTemplate = "/products/{productID}", ResponseFormat = WebMessageFormat.Xml)]
        public Review[] GetReviews(string productID)
        {
            return reviews.Where(r => r.ProductID == productID).ToArray();
        }
    }

    /// <summary>
    /// This class will contain the actual server process that hosts the service. Windows Communication 
    /// Foundation comes with its own in-process server, so every windows application can simply 
    /// host a web service. Alternatively, we can host our application in an IIS server (later more)
    /// </summary>

    class Program
    {
        static void Main(string[] args)
        {
            // We first create an instance of the service
            ProductReviewService reviewService = new ProductReviewService();

            // We then add two dummy reviews
            reviewService.reviews.Add(new Review("42", "123", "HappyCustomer", "Great product!", 5, 700));
            reviewService.reviews.Add(new Review("43", "123", "AngryCustomer", "What a piece of junk!", 1, 0));

            // We now create a web service host, that will use the service instance that we just created
            ServiceHost host = new ServiceHost(reviewService, new Uri("http://localhost:8001/"));

            // In WCF, a single service can have multiple endpoints and each of these endpints can have a so-called behavior 
            // that specifies what it does. In our case, our service will have the following three endpoints:
            
            // 1.) A REST endpoint, which allows us to access product reviews via a RESTful API
            // 2.) A SOAP Web Service endpoint, which allows us to generate a SOAP-based client (this is more RPC flavor)
            // 3.) A MetaData endpoint that will serve a WSDL description of the SOAP Web Service for clients 

            // Let us see how we can do this ... 

            // 1.) Add an endpoint for the RESTful service and specifiy that it should have as a default WebHttp endpoint    
            ServiceEndpoint rest = host.AddServiceEndpoint(typeof(ProductReviewService), new WebHttpBinding(), "rest");
            rest.EndpointBehaviors.Add(new WebHttpBehavior());

            // 2.) Add an endpoint for the SOAP Web Service (using Http as transport protocol)
            ServiceEndpoint soap = host.AddServiceEndpoint(typeof(ProductReviewService), new WSHttpBinding(), "soap");

            // 3.) Add a metadata endpoint that allows to obtain WSDL description of the SOAP service via HTTP Get
            ServiceMetadataBehavior smb = new ServiceMetadataBehavior();
            smb.HttpGetEnabled = true;
            host.Description.Behaviors.Add(smb);
            host.AddServiceEndpoint(ServiceMetadataBehavior.MexContractName, MetadataExchangeBindings.CreateMexHttpBinding(), "mex");
            
            // We are now ready to start listening for HTTP requests, until ENTER is pressed 
            host.Open();
            Console.WriteLine("Service is running");
            Console.WriteLine("Press enter to quit...");
            Console.ReadLine();

            // While the process is running, you can access the URL http://localhost:8001/?wsdl from your browser to see the WSDL 
            // description of the SOAP Web Service. This WSDL document can now be used to generate a SOAP-based client

            // Based on the URITemplates specified above, the REST API can be accessed for instance 
            // at http://localhost:8001/rest/products/123/MostHelpfulReview

            // Stop listening to requests
            host.Close();
        }
    }
}
