
recorder Node 
    """
    Record the response of a number of nodes at every converged step.

    RETURNS

    >0 an integer tag that can be used as a handle on the recorder for the remove recorder commmand.

    -1 recorder command failed if integer -1 returned.


    NOTES

    - Only one of -file, -xml, -binary, -tcp will be used. If multiple specified 
      last option is used.

    - In case you want to remove a recorder, you need to know the tag for that recorder. Here is an example on how to get the tag of a recorder:

          set tagRc [recorder Node -file nodesD.out -time -node 1 2 3 4 -dof 1 2 disp]


    EXAMPLES

    Generates output file `nodesD.out` that contains relative displacements in x
    and y direction at nodes 1, 2, 3, and 4. The output file will contain 9
    columns (time, disp. in x at node 1, disp. in y at node 1, ... , disp. in y
    at node 4))

       recorder Node -file nodesD.out -time -node 1 2 3 4 -dof 1 2 disp;


    For a `UniformExcitation` analysis, this command generates output file
    nodesA.out that contains absolute accelerations (ground motion acceleration
    + relative acceleration) in x direction for nodes 1, 2, 3, and 4. NOTE that
    if no TimeSeries is provided and a uniform excitation analysis is
    performed, the relative accelerations are recorded.

       recorder Node -file nodesA.out -timeSeries 1 -time -node 1 2 3 4 -dof 1 accel;

    """

    Alt("file_name", [
        Str(<-file $fileName>), 
        Str(<-xml $fileName>),
        Str(<-binary $fileName>)
      ],
      reqd=True,
      about="name of file to which output is sent."\
            "file output is either in xml format (-xml option), textual (-file option) or binary (-binary option)"
    ),

    <-tcp $inetAddress $port> 
        inetAddr     ip address, "xx.xx.xx.xx", of remote machine to which data is sent
        $port        port on remote machine awaiting tcp

    Int("precision", reqd=False, flag="-precision"
        about="number of significant digits (optional, default is 6)"\
              "(optional, default: records at every time step)"
    ),

    Ref("series", flag="-timeSeries", typ=TimeSeries,
        about="the tag of a previously constructed TimeSeries, results from node at each time step are added to load factor from series"
    ),

    Flg("-time>",
        about="optional, using this option places domain time in first entry of each data line, default is to have time ommitted"
    ),

    Num("time_step", flag="-dT",
        about="time interval for recording. will record when next step is `deltaT` greater than last recorder step."
    ),

    <-closeOnWrite> 
        -closeOnWrite    optional. using this option will instruct the recorder to invoke a close on the data handler after every timestep. If this is a file it will close the file on every step and then re-open it for the next step. Note, this greatly slows the execution time, but is useful if you need to monitor the data during the analysis.

    <-node $node1 $node2...> 
        $node1 $node2..    tags of nodes whose response is being recorded (optional, default: omitted)

    <-nodeRange $startNode $endNode> 
        $startNode $endNode..    tag for start and end nodes whose response is being recorded (optional, default: omitted)

    <-region $regionTag> 
        $regionTag       a region tag; to specify all nodes in the previously defined region. (optional)

    -dof ($dof1 $dof2 ...) 
        $dof1 dof2...    the specified dof at the nodes whose response is requested.


    $respType         a string indicating response required. Response types are given in table below.
        disp              displacement*
        vel               velocity*
        accel             acceleration*
        incrDisp          incremental displacement
        "eigen i"         eigenvector for mode i
        reaction          nodal reaction
        rayleighForces    damping forces



recorder Element 
    """
    The Element recorder type records the response of a number
    of elements at every converged step. The response recorded is element-dependent
    and also depends on the arguments which are passed to the setResponse() element
    method.

    RETURNS

    >0 an integer tag that can be used as a handle on the recorder for the remove recorder commmand.

    -1 recorder command failed if integer -1 returned.


    NOTE:

    The setResponse() element method is dependent on the element type, and is described with the Element Command.


    EXAMPLE

        recorder Element -file Element1.out -time -ele 1 3 section 1 fiber 0.10 0.10 stressStrain
    """

    <-file $fileName> <-xml $fileName> <-binary $fileName> 
        $fileName	name of file to which output is sent.
                    file output is either in xml format (-xml option), textual (-file option) or binary (-binary option)
    <-precision $nSD> 
        $nSD	    number of significant digits (optional, default is 6)
    <-time> 
        -time	    (optional using this option places domain time in first entry of each data line, default is to have time ommitted)
    <-closeOnWrite> 
        -closeOnWrite	optional. using this option will instruct the recorder to invoke a close on the data handler after every timestep. If this is a file it will close the file on every step and then re-open it for the next step. Note, this greatly slows the execution time, but is useful if you need to monitor the data during the analysis.
    <-dT $deltaT> 
        $deltaT	time interval for recording. will record when next step is $deltaT greater than last recorder step. (optional, default: records at every time step)
    <-ele ($ele1 $ele2 ...)> 
        $ele1 $ele2 ..	tags of elements whose response is being recorded -- selected elements in domain (optional, default: omitted)
    <-eleRange $startEle $endEle> 
        $startEle $endEle ..	tag for start and end elements whose response is being recorded -- range of selected elements in domain (optional, default: omitted)
    <-region $regTag> 
        $regTag	previously-defined tag of region of elements whose response is being recorded -- region of elements in domain (optional)
    $arg1 $arg2 ...
        $arg1 $arg2 ...	arguments which are passed to the `setResponse()` element method


