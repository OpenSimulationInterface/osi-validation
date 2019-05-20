<!DOCTYPE html>
<html>

<head>
    <style>
        #myInput {
            width: 100%;
            font-size: 16px;
            padding: 12px 20px;
            border: 1px solid #ddd;
            margin-bottom: 12px;
        }

        #myUL {
            /* Remove default list styling */
            list-style-type: none;
            padding: 0;
            margin: 0;
        }

        #myUL li a {
            border: 1px solid #ddd;
            margin-top: -1px;
            background-color: #f6f6f6;
            padding: 12px;
            text-decoration: none;
            font-size: 18px;
            color: black;
            display: block;
        }

        #myUL li a:hover:not(.header) {
            background-color: #eee;
        }
    </style>
</head>

<body>
    <h1>KPIs documentation</h1>
    <input type="text" id="myInput" onkeyup="myFunction()" placeholder="Search for names..">

    {elt_list}

    <script>
        function myFunction() {
            // Declare variables
            var input, filter, ul, li, a, i, txtValue;
            input = document.getElementById('myInput');
            filter = input.value.toUpperCase().split(' ');
            ul = document.getElementById("myUL");
            li = ul.getElementsByTagName('li');

            // Loop through all list items, and hide those who don't match the search query
            for (i = 0; i < li.length; i++) {
                a = li[i].getElementsByTagName("a")[0];
                txtValue = (a.textContent || a.innerText).toUpperCase();
                
                found = true
                filter.forEach(element => {
                    if (txtValue.search(element) === -1)
                        found = false
                });
                if (found) {
                    li[i].style.display = "";
                } else {
                    li[i].style.display = "none";
                }
            }
        }
    </script>
</body>

</html>