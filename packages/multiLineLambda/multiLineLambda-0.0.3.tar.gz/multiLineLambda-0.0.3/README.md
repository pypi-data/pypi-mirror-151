# Multiline lambda Function

Multiline lambda function in python. Give arguments to lambdafunction() and include multiple lines in a single lambda function.

<h2>Syntax :</h2>
General Syntax : 
<code>lambdaFunction.lambdafunction("list of string arguments", caller="string argument which gets calls the function.")</code>
<br>
<ul>
<li>First list of arguements should be wrapped in single function.</li>
   eg. <code>lambdaFunction.lambdafunction("def add(x, y) :","...", caller="...")</code>
<li>All the syntax should be same as python. Use "\t" for indentation</li>
<li>Function should have some return method.</li>
   eg. <code>lambdaFunction.lambdafunction("def add(x, y) :","\n\treturn(x+y)", caller="...")</code>
<li>Then pass the function name to caller. (Here, "add")</li>
   eg. <code>lambdaFunction.lambdafunction("def add(x, y) :","\n\treturn(x+y)", caller="add(3, 6)")</code>
       returns -> 18
       <br>
       when, <code>print(lambdaFunction.lambdafunction("def add(x, y) :","\n\treturn(x+y)", caller="add(3, 6)"))</code>
       prints -> 18.
</ul>
