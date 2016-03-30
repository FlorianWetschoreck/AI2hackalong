<!-- This is our XSL Transformation that will 
     transform the XML document into the HTML body 
     -->

<xsl:stylesheet version="1.0"
       xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
       xmlns:ps="http://schemas.datacontract.org/2004/07/ReviewService"
       exclude-result-prefixes="ps">
  <xsl:template match="/">
    <h1>
      <xsl:value-of select="/ps:Review/ps:User[1]/text()" />
    </h1>
    <h2>
      <xsl:value-of select="/ps:Review/ps:Rating[1]/text()" />/5 stars
    </h2>
    <p>
      <xsl:value-of select="/ps:Review/ps:ReviewText[1]/text()" />
    </p>
    <br />
  </xsl:template>
</xsl:stylesheet>
  