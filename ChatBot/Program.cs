// See: https://platform.openai.com/docs/guides/chat/introduction
// See: https://platform.openai.com/docs/api-reference/chat

using Azure;
using Azure.AI.OpenAI;
using Microsoft.Extensions.Configuration;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Spectre.Console;
using System;
using System.Text;

var builder = new ConfigurationBuilder()
    .AddUserSecrets<Program>();

var configuration = builder.Build();

string key = configuration["openaikey"];
string endpoint = configuration["endpoint"];
var client = new OpenAIClient(new Uri(endpoint), new AzureKeyCredential(key));
var deployment = configuration["deployment"];

// Define the API parameters
string baseAddress = "http://localhost:999/";
string kbEndpoint = "searchChromaDB";

static async Task<string> ConnectToLocalAPI(string baseAddress, string endpoint, string requestData)
{
    string responseBody = string.Empty;

    // Create an instance of HttpClient
    using (HttpClient client = new HttpClient())
    {
        try
        {
            // Set the base address of the API
            client.BaseAddress = new Uri(baseAddress);

            // Prepare the request content
            var content = new StringContent(requestData, Encoding.UTF8, "application/json");

            // Make a POST request to the API endpoint
            HttpResponseMessage response = await client.PostAsync(endpoint, content);

            // Check if the request was successful
            if (response.IsSuccessStatusCode)
            {
                // Read the response content as a string
                responseBody = await response.Content.ReadAsStringAsync();

                // Parse the JSON array
                JArray jsonArray = JArray.Parse(responseBody);

                // Get the first JSON object
                JObject firstObject = jsonArray.FirstOrDefault()?.ToObject<JObject>();

                // Get the value of the "body" property from the first object
                if (firstObject != null)
                {
                    responseBody = firstObject["body"].ToString();
                }

                // Do something with the response
                //Console.WriteLine(responseBody);
            }
            else
            {
                Console.WriteLine($"Request failed with status code: {response.StatusCode}");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"An error occurred: {ex.Message}");
        }
    }

    return responseBody;
}

string system = File.ReadAllText(@"system_seymour.txt");

AnsiConsole.MarkupLine($"[Magenta]SEYMOUR:[/] [white]{"Hello, I'm Seymour. How can I help you?"}[/]");

var completionOptions = new ChatCompletionsOptions();
completionOptions.Temperature = 0;
completionOptions.Messages.Add(new ChatMessage(ChatRole.System, system));
while (true)
{
    // Capture the users messages and add to
    // messages list for submitting to the chat API
    var userMessage = AnsiConsole.Ask<string>($"[Cyan]USER:[/] ");

    completionOptions.Messages.Add(new ChatMessage(ChatRole.User, userMessage));

    // go get kb string
    string jsonString = JsonConvert.SerializeObject(new { query = userMessage });
    string kbString = await ConnectToLocalAPI(baseAddress, kbEndpoint, jsonString);
    // replace kb var with bk info
    string updatedSystem = system.Replace("<<KB>>", kbString);

    completionOptions.Messages.Add(new ChatMessage(ChatRole.System, updatedSystem));
    try
    {
        AnsiConsole.MarkupLine($"[Grey]{"   thinking..."}[/]");
        Response<ChatCompletions> response = client.GetChatCompletions(deployment, completionOptions);
        string completion = response.Value.Choices[0].Message.Content;
        completionOptions.Messages.Add(new ChatMessage(ChatRole.Assistant, completion));
        //var messageObject = responseObject?.choices[0].message;
        AnsiConsole.MarkupLine($"[Magenta]SEYMOUR:[/] [white]{Markup.Escape(completion)}[/]");
    }
    catch (Exception ex)
    {
        Console.WriteLine(ex);
    }
}