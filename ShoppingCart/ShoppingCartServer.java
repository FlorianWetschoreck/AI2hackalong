import ShoppingCartApp.*;
import org.omg.CosNaming.*;
import org.omg.CosNaming.NamingContextPackage.*;
import org.omg.CORBA.*;
import org.omg.PortableServer.*;
import org.omg.PortableServer.POA;
import java.util.ArrayList;

import java.util.Properties;

class ShoppingCartImpl extends ShoppingCartPOA {
  private ORB orb;
  
  ArrayList<ShoppingCartEntry> contents = new ArrayList<ShoppingCartEntry>();

  public void setORB(ORB orb_val) {
    orb = orb_val; 
  }
    
  public void getShoppingCartContents(cartContentsHolder holder) {	
	// Here we are using an output parameter, i.e. we return the value 
	// by assigning the value to the argument
    ShoppingCartEntry[] arr = new ShoppingCartEntry[contents.size()];
	arr = contents.toArray(arr);
	holder.value = arr;
	System.out.println("Returning shopping cart contents");
  }  
  
  public void addToShoppingCart(String productId, int amount) {
    ShoppingCartEntry e = new ShoppingCartEntry();
    e.productID = productId;
    e.amount = amount;
    contents.add(e);
	System.out.println("Added product to shopping cart");
  }
  
  public void updateAmount(String productId, int new_amount) {
    for (ShoppingCartEntry entry: contents) {
		if (entry.productID.equals(productId))
		{
			entry.amount = new_amount;
			System.out.println("Updated amount");
		}
	}
  }
  
  public void clearShoppingCart()
  {
    contents.clear();
	System.out.println("Cleared shopping cart");
  }

  public void shutdown() {
    orb.shutdown(false);
  }
}


public class ShoppingCartServer {

  public static void main(String args[]) {
    try{
      // create and initialize the ORB
      ORB orb = ORB.init(args, null);

      // get reference to rootpoa & activate the POAManager
      POA rootpoa = POAHelper.narrow(orb.resolve_initial_references("RootPOA"));
      rootpoa.the_POAManager().activate();

      // create servant and register it with the ORB
      ShoppingCartImpl ShoppingCartImpl = new ShoppingCartImpl();
      ShoppingCartImpl.setORB(orb); 

      // get object reference from the servant
      org.omg.CORBA.Object ref = rootpoa.servant_to_reference(ShoppingCartImpl);
      ShoppingCart href = ShoppingCartHelper.narrow(ref);
          
      // get the root naming context
      // NameService invokes the name service
      org.omg.CORBA.Object objRef =
          orb.resolve_initial_references("NameService");
      // Use NamingContextExt which is part of the Interoperable
      // Naming Service (INS) specification.
      NamingContextExt ncRef = NamingContextExtHelper.narrow(objRef);

      // bind the Object Reference in Naming
      String name = "ShoppingCart";
      NameComponent path[] = ncRef.to_name( name );
      ncRef.rebind(path, href);

      System.out.println("ShoppingCartServer running at " + orb.object_to_string(href));

      // wait for invocations from clients
      orb.run();
    } 
        
      catch (Exception e) {
        System.err.println("ERROR: " + e);
        e.printStackTrace(System.out);
      }
          
      System.out.println("ShoppingCartServer Exiting ...");
        
  }
}
