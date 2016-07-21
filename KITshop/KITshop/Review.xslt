<!-- This is our XSL Transformation that will 
     transform the XML document into HTML elements
     -->

<xsl:stylesheet version="1.0"
       xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
       xmlns:ps="http://schemas.datacontract.org/2004/07/ReviewService"
       exclude-result-prefixes="ps">
  
   <xsl:output omit-xml-declaration="yes"/>
    
  <xsl:template match="/">    
      <h1>
        Review from <xsl:value-of select="/ps:Review/ps:User[1]/text()" />
      </h1>
      <p class="stars">
        <xsl:value-of select="/ps:Review/ps:Rating[1]/text()" />/5 stars
      </p>
      <p>
        <xsl:value-of select="/ps:Review/ps:ReviewText[1]/text()" />
      </p>
  </xsl:template>
</xsl:stylesheet>
  