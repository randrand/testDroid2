package com.example.gaedbclient;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.io.BufferedReader;
import java.io.InputStreamReader;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;
import org.apache.http.NameValuePair;
import org.json.JSONArray;
import org.json.JSONException;
//import org.apache.commons.compress.utils.IOUtils;

import com.example.gaedbclient.R;

import android.os.AsyncTask;
import android.os.Bundle;
import android.app.Activity;
import android.view.Menu;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.view.KeyEvent;
import android.view.inputmethod.EditorInfo;


public class MainActivity extends Activity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		
		Button storeButton = (Button)findViewById(R.id.button1);
		storeButton.setOnClickListener(new View.OnClickListener() {
        	public void onClick(View v) {
        		
        		//ArrayList<String> passing = new ArrayList<String>();
        		//passing.add(fieldKey);
        		//passing.add(fieldVal);
        		String[ ] aStr = new String[2] ;
        		aStr[0] = ((EditText)findViewById(R.id.fieldInKey)).getText().toString();
        		aStr[1] = ((EditText)findViewById(R.id.fieldInVal)).getText().toString();
        		String[ ] rStr = new String[1] ;
        		rStr[0] = ((EditText)findViewById(R.id.inQKey)).getText().toString();
        		
        		if (!aStr[0].isEmpty() && !aStr[1].isEmpty())
        		{
        			httpStore hS = new httpStore();
        			hS.execute(aStr);
        		}
        		else if (!rStr[0].isEmpty())
        		{
        			httpQuery hQ = new httpQuery();
            		hQ.execute(rStr);
        		}
        	}
        }
        );
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}
	
	protected class httpStore extends AsyncTask<String, Void, Void> {
		@Override
		protected Void doInBackground(String... strs) {
			// Sample HTTP POST request code:
			// http://www.androidhive.info/2011/10/android-making-http-requests/
			// http://www.softwarepassion.com/android-series-get-post-and-multipart-post-requests/
			// Debugging server side using curl:
			// http://stackoverflow.com/questions/1087185/http-testing-tool-easily-send-post-get-put
			String temp1="";
			HttpClient httpclient = new DefaultHttpClient();

			HttpPost storeVal = new HttpPost("http://dearbabymaimai.appspot.com/modify");
			
			// ArrayList<NameValuePair> is used to send values from android app to server.
		        ArrayList<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();  
		        
		        // "tag" is the name of the text form on the webserver
		        // "mytagInput" is the value that the client is submitting to the server
		        nameValuePairs.add(new BasicNameValuePair("tag", strs[0]));
		        nameValuePairs.add(new BasicNameValuePair("value", strs[1]));  

		      
				 try {
					 UrlEncodedFormEntity httpEntity = new UrlEncodedFormEntity(nameValuePairs);
					 storeVal.setEntity(httpEntity); 
					 
					 HttpResponse response = httpclient.execute(storeVal);

					 temp1 = EntityUtils.toString(response.getEntity());				
					} 
					  catch (ClientProtocolException e) {			  
						e.printStackTrace();
					} catch (IOException e) {
						System.out.println("HTTP IO Exception");
						e.printStackTrace();
					}
					 

		            // Decode the JSON array. Array is zero based so the return value is in element 2
					try {
						JSONArray jsonArray = new JSONArray(temp1);
						//if (jsonArray.getString(0) != "STORED")
						//	return null;
						
					} catch (JSONException e) {
						System.out.println("Error in JSON decoding");
						e.printStackTrace();
					} 
					
			return null;
		}
		@Override
		protected void onPostExecute(Void unused) {
			((EditText)findViewById(R.id.fieldInKey)).setText("");
			((EditText)findViewById(R.id.fieldInVal)).setText("Stored!");
		}
	}

	protected class httpQuery extends AsyncTask<String, Void, String> {
		String reply = null;
		@Override
		protected String doInBackground(String... strs) {
			String temp1="";
			HttpClient httpclient = new DefaultHttpClient();

				HttpPost getVal = new HttpPost("http://dearbabymaimai.appspot.com/query");
			
				// ArrayList<NameValuePair> is used to send values from android app to server.
		        ArrayList<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();  
		        
		        // "tag" is the name of the text form on the webserver
		        // "mytagInput" is the value that the client is submitting to the server
		        nameValuePairs.add(new BasicNameValuePair("tag", strs[0]));
		        
		      
				 try {
					 UrlEncodedFormEntity httpEntity = new UrlEncodedFormEntity(nameValuePairs);
					 getVal.setEntity(httpEntity); 
					 
					 //ResponseHandler<String> responseHandler = new BasicResponseHandler();
					 
					 HttpResponse response = httpclient.execute(getVal);
					 temp1 = EntityUtils.toString(response.getEntity());
						//statuscode = response.getStatusLine().getStatusCode();
						
					} 
					  catch (ClientProtocolException e) {			  
						e.printStackTrace();
					} catch (IOException e) {
						System.out.println("HTTP IO Exception");
						e.printStackTrace();
					}
					 

		            // Decode the JSON array. Array is zero based so the return value is in element 2
					try {
						JSONArray jsonArray = new JSONArray(temp1);
						reply = jsonArray.getString(2);
						return reply;
					} catch (JSONException e) {
						// TODO Auto-generated catch block
						System.out.println("Error in JSON decoding");
						e.printStackTrace();
					} 
					
			return null;
		}
		@Override
		protected void onPostExecute(String res) {
			((TextView)findViewById(R.id.outVal)).setText("Temperature: "+res);
		}
	}
}
