package kitshop_orderprocessor;

import javax.jms.ExceptionListener;
import javax.jms.JMSException;
import javax.jms.Connection;
import javax.jms.Destination;
import javax.jms.Message;
import javax.jms.MessageConsumer;
import javax.jms.Session;
import javax.jms.TextMessage;
import javax.jms.BytesMessage;

import org.apache.activemq.ActiveMQConnectionFactory;


/**
 *
 * @author Ingo Scholtes
 */
public class KITShop_OrderProcessor {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Thread brokerThread = new Thread(new OrderMsgConsumer());
        brokerThread.setDaemon(false);
        
        System.out.println("Waiting for messages");
        brokerThread.start();                      
    }
    
    
    public static class OrderMsgConsumer implements Runnable, ExceptionListener {
        public void run() {            
            try {
                ActiveMQConnectionFactory connectionFactory = new ActiveMQConnectionFactory("tcp://localhost:61616");

                // Create a Connection
                Connection connection = connectionFactory.createConnection();
                connection.start();

                connection.setExceptionListener(this);

                Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);

                Destination destination = session.createQueue("KITShop_OrderBook");
                MessageConsumer consumer = session.createConsumer(destination);

                boolean finish = false;
                
                while(!finish) {
                    Message message = consumer.receive();


                    if (message instanceof TextMessage) {
                            TextMessage textMessage = (TextMessage) message;
                            String text = textMessage.getText();
                            System.out.println("Received: " + text);
                    } else if (message instanceof BytesMessage) {
                            BytesMessage byteMessage = (BytesMessage) message;
                            byte[] byteArr = new byte[(int)byteMessage.getBodyLength()];
                            byteMessage.readBytes(byteArr); 
                            String text = new String(byteArr, "UTF-8");  
                            System.out.println("Received: " + text);
                    }
                    
                }
                consumer.close();
                session.close();
                connection.close(); 
            }
            catch (Exception e) {
                System.out.println("Caught: " + e);
                e.printStackTrace();
            }
        }
        
    public synchronized void onException(JMSException ex) {
            System.out.println("JMS Exception occured.  Shutting down client.");
        }
}
    
}
