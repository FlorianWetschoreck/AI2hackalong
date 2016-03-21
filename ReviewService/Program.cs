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
   
    // This struct contains all information of a single product review
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
   
    // This is the main Product Review service
    // The attributes tell Windows Communication Foundation how to expose the methods as 
    // service operations. Here we expose the methods both as a SOAP, as well as as RESTful Web Service
    // The mapping of REST URIs to service methods is done via the WebGet attribute
    [ServiceContract()]
    [ServiceBehavior(InstanceContextMode =InstanceContextMode.Single)]
    public class ReviewService
    {
        public List<Review> reviews = new List<Review>();

        [OperationContract]
        [WebGet(UriTemplate = "GetAvgRating/{productID}")]
        public double GetAvgRating(string productID)
        {
            return reviews.Where(r => r.ProductID == productID).Select(r => r.Rating).Average();
        }

        [OperationContract]
        [WebGet(UriTemplate = "GetMostHelpfulReview/{productID}")]
        public Review GetMostHelpfulReview(string productID)
        {
            return reviews.OrderByDescending(x => x.HelpfulVotes).First();
        }

        [OperationContract]
        [WebGet(UriTemplate = "GetReview/{reviewID}")]
        public Review GetReview(string reviewID)
        {
            return reviews.Where(r => r.ReviewID == reviewID).First();
        }

        [OperationContract]
        [WebGet(UriTemplate = "GetReviews/{productID}")]
        public Review[] GetReviews(string productID)
        {
            return reviews.Where(r => r.ProductID == productID).ToArray();
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            // Create an instance of the service
            ReviewService reviewService = new ReviewService();

            // Add two dummy reviews to the service
            reviewService.reviews.Add(new Review("42", "123", "HappyCustomer", "Great product!", 5, 700));
            reviewService.reviews.Add(new Review("43", "123", "AngryCustomer", "What a piece of junk!", 1, 0));

            // Create a web service host, that will answer to HTTP requests 
            WebServiceHost host = new WebServiceHost(reviewService, new Uri("http://localhost:8001/"));

            // add two endpoints for the SOAP and the REST Web Service
            ServiceEndpoint soap = host.AddServiceEndpoint(typeof(ReviewService), new BasicHttpBinding(), "soap");            
            ServiceEndpoint rest = host.AddServiceEndpoint(typeof(ReviewService), new WebHttpBinding(), "rest");            

            // Start listening for HTTP requests, until ENTER is pressed 
            host.Open();
            Console.WriteLine("Service is running");
            Console.WriteLine("Press enter to quit...");
            Console.ReadLine();

            // Stop listening to requests
            host.Close();
        }
    }
}
