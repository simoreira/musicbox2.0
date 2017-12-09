<?xml version="1.0"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:topP="http://www.topPortugal.com/tracks#" xmlns:foaf="http://xmlns.com/foaf/spec/">

  <xsl:template match="/">
    <rdf:RDF>
      <rdf:Description rdf:about="http://www.topPortugal.com/tracks">
        <xsl:apply-templates/>
      </rdf:Description>
    </rdf:RDF>
  </xsl:template>

  <xsl:template match="track">
    <xsl:variable name="track"><xsl:value-of select="name"/></xsl:variable>
    <xsl:variable name="name"><xsl:value-of select="artist/name"/></xsl:variable>
    <xsl:variable name="imgSmall"><xsl:value-of select="image[@size='small']"/></xsl:variable>
    <xsl:variable name="imgMedium"><xsl:value-of select="image[@size='medium']"/></xsl:variable>
    <xsl:variable name="imgLarge"><xsl:value-of select="image[@size='large']"/></xsl:variable>
    <xsl:variable name="imgExtraLarge"><xsl:value-of select="image[@size='extralarge']"/></xsl:variable>

    <topP:track>
      <rdf:Description rdf:about="http://www.topPortugal.com/tracks/{$track}">
        <foaf:name><xsl:value-of select="name"/></foaf:name>
        <topP:listeners><xsl:value-of select="listeners"/></topP:listeners>
        <topP:duration><xsl:value-of select="duration"/></topP:duration>
        <topP:url><xsl:value-of select="url"/></topP:url>
        <topP:imgSmall><xsl:value-of select="$imgSmall"/></topP:imgSmall>
        <topP:imgMedium><xsl:value-of select="$imgMedium"/></topP:imgMedium>
        <topP:imgLarge><xsl:value-of select="$imgLarge"/></topP:imgLarge>
        <topP:imgExtraLarge><xsl:value-of select="$imgExtraLarge"/></topP:imgExtraLarge>

        <xsl:for-each select="artist">
          <topP:artist>
            <rdf:Description rdf:about="http://www.topPortugal.com/tracks/{$track}/artist/{$name}">
              <foaf:name_artist><xsl:value-of select="name"/></foaf:name_artist>
            </rdf:Description>
          </topP:artist>
        </xsl:for-each>
      </rdf:Description>
    </topP:track>
  </xsl:template>

</xsl:stylesheet>
